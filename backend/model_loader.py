import os
import pickle
import numpy as np
from pathlib import Path
import logging
from typing import Dict, Any, Optional
import json

logger = logging.getLogger(__name__)


class ModelLoader:
    """
    Carrega e gerencia o modelo de IA para detecção de tiros
    """

    def __init__(self):
        self.model = None
        # usar pasta local ./models para facilitar desenvolvimento
        self.model = None
        self.model_path = Path("models")
        self.model_file = self.model_path / "gunshot_detector.pkl"
        self.config_file = self.model_path / "model_metadata.json"
        self.scaler_file = self.model_path / "scaler.joblib"
        self.model_info = {}
        self.feature_extractor = None

        # Criar diretório de modelos se não existir
        self.model_path.mkdir(exist_ok=True)

        # Tentar carregar o modelo
        self.load_model()

    def load_model(self):
        """Carrega o modelo treinado"""
        try:
            if self.model_file.exists():
                with open(self.model_file, "rb") as f:
                    self.model = pickle.load(f)

                # Carregar configuração
                if self.config_file.exists():
                    with open(self.config_file, "r") as f:
                        self.model_info = json.load(f)
                # Carregar scaler se existir
                try:
                    import joblib

                    if self.scaler_file.exists():
                        self.feature_scaler = joblib.load(self.scaler_file)
                        logger.info(f"✓ Scaler carregado: {self.scaler_file}")
                except Exception:
                    logger.info("Scaler não encontrado ou falha ao carregar scaler")

                logger.info(f"✓ Modelo ML carregado: {self.model_file}")
                logger.info(f"✓ Tipo: {self.model_info.get('model_type', 'Unknown')}")
                logger.info(
                    f"✓ Features: {self.model_info.get('feature_dim', 'Unknown')}"
                )
            else:
                logger.warning(
                    "⚠️  Modelo treinado não encontrado. Usando modelo baseado em regras."
                )
                logger.info(
                    "💡 Para treinar um modelo: python ml/train_gunshot_detector.py"
                )
                self._load_default_model()

        except Exception as e:
            logger.error(f"❌ Erro ao carregar modelo: {e}")
            self._load_default_model()

    def _load_default_model(self):
        """Carrega um modelo padrão baseado em regras"""
        logger.info("Carregando modelo padrão baseado em regras")
        self.model = "rule_based"
        self.model_info = {
            "name": "Rule-Based Detector",
            "version": "1.0.0",
            "type": "rule_based",
            "description": "Detector baseado em características de áudio",
            "trained_date": "N/A",
            "accuracy": "N/A",
        }

    def predict(self, audio_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Faz predição usando o modelo carregado
        """
        try:
            if self.model == "rule_based" or self.model is None:
                return self._rule_based_prediction(audio_features)
            else:
                return self._ml_prediction(audio_features)

        except Exception as e:
            logger.error(f"Erro na predição: {e}")
            return {
                "gunshot_detected": False,
                "confidence": 0.0,
                "probability": 0.0,
                "risk_level": "unknown",
                "error": str(e),
            }

    def _rule_based_prediction(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predição baseada em regras de características de áudio
        """
        # Características típicas de tiros
        gunshot_detected = False
        confidence = 0.0
        detections = []

        # Regra 1: Pico de energia alto
        if features.get("energy", 0) > 0.7:
            confidence += 0.3
            gunshot_detected = True

        # Regra 2: Frequência característica (100-4000 Hz)
        peak_freq = features.get("peak_frequency", 0)
        if 100 <= peak_freq <= 4000:
            confidence += 0.25
            gunshot_detected = True

        # Regra 3: Zero crossing rate alto (transiente rápido)
        zcr = features.get("zero_crossing_rate", 0)
        if zcr > 0.15:
            confidence += 0.2
            gunshot_detected = True

        # Regra 4: Espectro de frequência característico
        spectral_centroid = features.get("spectral_centroid", 0)
        if spectral_centroid > 2000:
            confidence += 0.25
            gunshot_detected = True

        # Determinar nível de risco
        if confidence >= 0.7:
            risk_level = "high"
        elif confidence >= 0.4:
            risk_level = "medium"
        elif confidence >= 0.2:
            risk_level = "low"
        else:
            risk_level = "none"
            gunshot_detected = False

        # Criar detecções simuladas se tiro detectado
        if gunshot_detected and confidence > 0.5:
            duration = features.get("duration", 0)
            num_detections = int(confidence * 3)  # 1-3 detecções

            for i in range(num_detections):
                detections.append(
                    {
                        "timestamp": round(
                            duration * (i + 1) / (num_detections + 1), 2
                        ),
                        "confidence": round(
                            confidence + np.random.uniform(-0.1, 0.1), 2
                        ),
                        "type": "gunshot",
                    }
                )

        return {
            "gunshot_detected": gunshot_detected,
            "confidence": round(confidence, 2),
            "probability": round(confidence, 2),
            "risk_level": risk_level,
            "detections": detections,
            "method": "rule_based",
        }

    def _ml_prediction(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predição usando modelo de Machine Learning treinado
        """
        try:
            # Import relativo ao pacote ml
            from ml.train_gunshot_detector import GunshotDetectorTrainer

            # Criar extrator com mesmos parâmetros do treinamento
            trainer = GunshotDetectorTrainer(
                sample_rate=self.model_info.get("sample_rate", 22050),
                n_mfcc=self.model_info.get("n_mfcc", 40),
                n_fft=self.model_info.get("n_fft", 2048),
                hop_length=self.model_info.get("hop_length", 512),
            )
            trainer.model = self.model

            # Extrair features do áudio original
            audio_path = features.get("audio_path")
            if not audio_path or not os.path.exists(audio_path):
                logger.error("Caminho do áudio não fornecido ou inválido")
                return self._rule_based_prediction(features)

            # Extrair features usando o mesmo método do treinamento
            feature_vector = trainer.extract_features(audio_path)

            if feature_vector is None:
                logger.error("Falha ao extrair features")
                return self._rule_based_prediction(features)

            # Fazer predição (aplicar scaler se disponível)
            feature_vector = feature_vector.reshape(1, -1)
            if hasattr(self, "feature_scaler") and self.feature_scaler is not None:
                feature_vector = self.feature_scaler.transform(feature_vector)
            prediction = self.model.predict(feature_vector)[0]
            probability = self.model.predict_proba(feature_vector)[0]

            gunshot_prob = probability[1] if len(probability) > 1 else probability[0]
            gunshot_detected = bool(prediction == 1)

            # Determinar nível de risco
            if gunshot_prob >= 0.8:
                risk_level = "high"
            elif gunshot_prob >= 0.5:
                risk_level = "medium"
            elif gunshot_prob >= 0.3:
                risk_level = "low"
            else:
                risk_level = "none"

            # Criar detecções se tiro detectado
            detections = []
            if gunshot_detected and gunshot_prob > 0.5:
                duration = features.get("duration", 0)
                detections.append(
                    {
                        "timestamp": round(duration / 2, 2),
                        "confidence": round(float(gunshot_prob), 2),
                        "type": "gunshot",
                    }
                )

            logger.info(
                f"🎯 Predição ML: {'TIRO' if gunshot_detected else 'NÃO-TIRO'} (confiança: {gunshot_prob:.2%})"
            )

            return {
                "gunshot_detected": gunshot_detected,
                "confidence": round(float(gunshot_prob), 2),
                "probability": round(float(gunshot_prob), 2),
                "risk_level": risk_level,
                "detections": detections,
                "method": "machine_learning",
                "model_type": self.model_info.get("model_type", "Unknown"),
            }

        except Exception as e:
            logger.error(f"Erro na predição ML: {e}")
            logger.info("Fallback para predição baseada em regras")
            return self._rule_based_prediction(features)

    def is_loaded(self) -> bool:
        """Verifica se o modelo está carregado"""
        return self.model is not None

    def get_model_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o modelo"""
        return {
            **self.model_info,
            "loaded": self.is_loaded(),
            "model_path": str(self.model_file),
        }
