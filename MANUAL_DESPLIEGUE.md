# MANUAL DE DESPLIEGUE Y PRUEBAS - OAKSGEN-ENGINEERING V2.0

## 1. Requisitos Técnicos
- Docker Desktop / Docker Compose
- Python 3.10+ (para desarrollo local en VS Code)

## 2. Despliegue Local (VS Code)
1. Instalar dependencias: `pip install -r requirements.txt`
2. Iniciar API: `uvicorn app.main:app --reload --port 8000`

## 3. Despliegue en la Nube (AWS / Cloud Run / Render)
1. Construir imagen: `docker build -t oaksgen-engineering:v2.0 .`
2. Subir a Registro y desplegar exponiendo el puerto `8000`.
