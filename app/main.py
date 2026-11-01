import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

from app.rag_engine import NormativeRAGEngine

app = FastAPI(
    title="OaksGen-Engineering API",
    description="Sistema MLOps de Inferencia e Inspección Industrial para Oaks Motors Industries",
    version="2.0.0"
)

rag_engine = NormativeRAGEngine()

MODEL_PATH = os.path.join("models", "xgboost_oaksgen.pkl")
SCALER_PATH = os.path.join("datos", "pipeline_scaler.pkl")

model = None
scaler = None

@app.on_event("startup")
def load_artifacts():
    global model, scaler
    try:
        if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
            model = joblib.load(MODEL_PATH)
            scaler = joblib.load(SCALER_PATH)
            print(">>> [INFO] Artefactos cargados exitosamente (.pkl).")
        else:
            print(">>> [WARNING] No se encontraron archivos .pkl. Modo simulado activo.")
    except Exception as e:
        print(f">>> [ERROR] Fallo al cargar artefactos: {str(e)}")

class InspectionDataInput(BaseModel):
    tipo_componente: str = Field(..., example="sheetmetal", description="Tipo de material: 'sheetmetal' o 'plastico'")
    gradiente_termico: float = Field(..., example=48.5, description="Temperatura durante el escaneo (°C)")
    potencia_mecanica: float = Field(..., example=125.0, description="Carga o fuerza aplicada (kW/N)")
    rugosidad_superficial: float = Field(..., example=1.35, description="Índice de rugosidad en micras (µm)")
    desviacion_geometrica: float = Field(..., example=0.62, description="Desviación dimensional respecto al CAD (mm)")

class PredictionResponse(BaseModel):
    clase_predicha: int
    estado_componente: str
    probabilidad_falla: float
    umbral_aplicado: float
    recomendacion_rag: Optional[dict] = None

@app.get("/", tags=["Health Check"])
def root():
    return {
        "sistema": "OaksGen-Engineering v2.0",
        "empresa": "Oaks Motors Industries",
        "estado": "Operativo",
        "modelo_cargado": model is not None
    }

@app.post("/predict", response_model=PredictionResponse, tags=["Inferencia MLOps"])
def predict_defect(data: InspectionDataInput):
    try:
        input_df = pd.DataFrame([{
            'gradiente_termico': data.gradiente_termico,
            'potencia_mecanica': data.potencia_mecanica,
            'rugosidad_superficial': data.rugosidad_superficial,
            'desviacion_geometrica': data.desviacion_geometrica
        }])

        if scaler is not None:
            features_scaled = scaler.transform(input_df)
        else:
            features_scaled = input_df.values

        if model is not None:
            prob_falla = float(model.predict_proba(features_scaled)[:, 1][0])
        else:
            termico_val = data.gradiente_termico > 52.0
            geom_val = data.desviacion_geometrica > 1.1
            prob_falla = 0.88 if (termico_val or geom_val) else 0.05

        UMBRAL_OPTIMO = 0.32
        es_falla = prob_falla >= UMBRAL_OPTIMO
        clase_final = 1 if es_falla else 0
        estado_str = "Falla Crítica" if es_falla else "Conforme"

        recomendacion = rag_engine.get_recommendation(
            tipo_material=data.tipo_componente,
            resultado_falla=estado_str
        )

        return PredictionResponse(
            clase_predicha=clase_final,
            estado_componente=estado_str,
            probabilidad_falla=round(prob_falla, 4),
            umbral_aplicado=UMBRAL_OPTIMO,
            recomendacion_rag=recomendacion
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante el proceso de inferencia: {str(e)}"
        )
