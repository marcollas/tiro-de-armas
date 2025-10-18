from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from pathlib import Path
import json
from datetime import datetime
import logging

from audio_processor import AudioProcessor
from model_loader import ModelLoader
from generate_audio_graphs import generate_audio_graphs

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Gunshot Detection API",
    description="API de detecção de tiros em áudio usando IA",
    version="1.0.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar processador de áudio e modelo
audio_processor = AudioProcessor()
model_loader = ModelLoader()

# Diretórios (usar pasta local para desenvolvimento)
UPLOAD_DIR = Path("temp")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
async def root():
    """Endpoint raiz - informações da API"""
    return {
        "service": "Gunshot Detection API",
        "version": "1.0.0",
        "status": "online",
        "model_loaded": model_loader.is_loaded(),
        "model_info": model_loader.get_model_info(),
    }


@app.get("/health")
async def health_check():
    """Health check para Docker"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_status": "loaded" if model_loader.is_loaded() else "not_loaded",
    }


@app.post("/api/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    """
    Analisa um arquivo de áudio para detectar tiros
    """
    try:
        # Validar tipo de arquivo
        allowed_extensions = [".wav", ".mp3", ".m4a", ".flac", ".ogg"]
        file_ext = Path(file.filename).suffix.lower()

        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Formato não suportado. Use: {', '.join(allowed_extensions)}",
            )

        # Salvar arquivo temporariamente (usar somente o nome do arquivo recebido)
        safe_name = Path(file.filename).name
        temp_file = UPLOAD_DIR / f"{datetime.now().timestamp()}_{safe_name}"

        with open(temp_file, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        logger.info(f"Arquivo recebido: {file.filename} ({len(content)} bytes)")

        # Processar áudio
        audio_features = audio_processor.extract_features(str(temp_file))

        # Fazer predição com o modelo
        prediction = model_loader.predict(audio_features)

        # gerar gráficos para analise
        print("Gerando gráficos para análise...")
        generate_audio_graphs(str(temp_file))

        # Limpar arquivo temporário
        try:
            if temp_file.exists():
                temp_file.unlink()
        except Exception:
            logger.warning(f"Não foi possível remover arquivo temporário: {temp_file}")

        # Retornar resultado
        return JSONResponse(
            content={
                "success": True,
                "filename": file.filename,
                "analysis": {
                    "gunshot_detected": prediction["gunshot_detected"],
                    "confidence": prediction["confidence"],
                    "probability": prediction["probability"],
                    "risk_level": prediction["risk_level"],
                    "method": prediction.get("method"),
                    "timestamp": datetime.now().isoformat(),
                },
                "audio_features": {
                    "duration": audio_features["duration"],
                    "sample_rate": audio_features["sample_rate"],
                    "channels": audio_features["channels"],
                    "peak_frequency": audio_features.get("peak_frequency"),
                    "energy": audio_features.get("energy"),
                },
                "detections": prediction.get("detections", []),
            }
        )
    except Exception as e:
        logger.error(f"Erro ao processar áudio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/batch-analyze")
async def batch_analyze(files: list[UploadFile] = File(...)):
    """
    Analisa múltiplos arquivos de áudio
    """
    results = []

    for file in files:
        try:
            result = await analyze_audio(file)
            results.append({"filename": file.filename, "success": True, "data": result})
        except Exception as e:
            results.append(
                {"filename": file.filename, "success": False, "error": str(e)}
            )

    return {"results": results}


@app.get("/api/model/info")
async def model_info():
    """Retorna informações sobre o modelo carregado"""
    return model_loader.get_model_info()


@app.post("/api/model/reload")
async def reload_model():
    """Recarrega o modelo de IA"""
    try:
        model_loader.load_model()
        return {
            "success": True,
            "message": "Modelo recarregado com sucesso",
            "model_info": model_loader.get_model_info(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
