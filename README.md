# OaksGen-Engineering v2.0 - Oaks Motors Industries
Sistema MLOps de Inferencia e Inspección Industrial para detección de fallas en componentes de Sheetmetal y Ornamentaciones de Plástico.

## Estructura del Repositorio
- `app/`: Código fuente de la API FastAPI y Motor RAG Normativo.
- `datos/`: Dataset procesado y artefacto del escalador (`pipeline_scaler.pkl`).
- `models/`: Modelo XGBoost serializado (`xgboost_oaksgen.pkl`).
- `Dockerfile` & `docker-compose.yml`: Configuración de contenerización.

## Ejecución Rápida en Local con Docker
```bash
docker-compose up --build -d
```
Accede a la API en: http://localhost:8000/docs
