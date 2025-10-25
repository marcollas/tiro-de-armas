import os
import pickle
import numpy as np
from pathlib import Path
import logging
from typing import Dict, Any
import json

# Imports opcionais para TensorFlow/Keras (carregamento preguiçoso)
try:
    import tensorflow as tf
    from tensorflow.keras.models import model_from_json
except Exception:  # pragma: no cover - ambiente sem TF
    tf = None
    model_from_json = None

logger = logging.getLogger(__name__)


class ModelLoader:
    """
    Carrega e gerencia o modelo de IA para detecção de tiros
    """

    def __init__(self):
        # Controle de estado
        self.model = None
        self.model_framework = None  # 'tf_keras' | 'sklearn' | 'rule_based'
        self.last_error: str | None = None

        # Artefatos sklearn legados (fallback)
        self.model_path = Path("models")
        self.model_file = self.model_path / "gunshot_detector.pkl"
        self.config_file = self.model_path / "model_metadata.json"
        self.scaler_file = self.model_path / "scaler.joblib"

        # Artefatos TF/Keras (novo modelo EfficientNet)
        self.tf_dir = Path("IA_EfficientNet_test")
        self.tf_config_path = self.tf_dir / "config.json"
        self.tf_weights_path = self.tf_dir / "model.weights.h5"

        self.model_info: Dict[str, Any] = {}

        # Garantir diretórios existentes quando aplicável
        self.model_path.mkdir(exist_ok=True)

        # Carregar modelo
        self.load_model()

    def load_model(self):
        """Carrega o modelo de IA (preferência para TF/Keras EfficientNet)."""
        # 1) Tenta carregar o modelo TF/Keras (IA_EfficientNet_test)
        try:
            if self.tf_config_path.exists() and self.tf_weights_path.exists():
                if tf is None or model_from_json is None:
                    raise RuntimeError(
                        "TensorFlow não está disponível no ambiente para carregar o modelo Keras."
                    )

                logger.info("Carregando modelo Keras (IA_EfficientNet_test)...")
                with open(self.tf_config_path, "r") as f:
                    config_json = f.read()
                keras_model = model_from_json(config_json)
                keras_model.load_weights(str(self.tf_weights_path))
                self.model = keras_model
                self.model_framework = "tf_keras"

                # Descobrir input shape do modelo
                try:
                    input_shape = getattr(self.model, "input_shape", None)
                except Exception:
                    input_shape = None

                self.model_info = {
                    "name": "IA_EfficientNet_test",
                    "version": "1.0",
                    "type": "keras_efficientnet",
                    "description": "Modelo Keras EfficientNet para detecção de tiros via espectrograma",
                    "input_shape": str(input_shape),
                    "path": str(self.tf_dir),
                    "framework": "tf.keras",
                }
                logger.info("✓ Modelo Keras carregado com sucesso")
                self.last_error = None
                return
        except Exception as e:
            logger.error(f"Falha ao carregar modelo Keras: {e}")
            try:
                # Guardar erro textual para inspeção via API
                self.last_error = str(e)
            except Exception:
                self.last_error = "Unknown error while loading Keras model"

        # 2) Fallback: tenta carregar modelo sklearn legado (se existir)
        try:
            # Desabilitar fallback sklearn se objetivo é usar TF
            if False and self.model_file.exists():
                with open(self.model_file, "rb") as f:
                    self.model = pickle.load(f)
                self.model_framework = "sklearn"

                if self.config_file.exists():
                    with open(self.config_file, "r") as f:
                        self.model_info = json.load(f)

                try:
                    import joblib

                    if self.scaler_file.exists():
                        self.feature_scaler = joblib.load(self.scaler_file)
                        logger.info(f"✓ Scaler carregado: {self.scaler_file}")
                except Exception:
                    logger.info("Scaler não encontrado ou falha ao carregar scaler")

                logger.info(f"✓ Modelo sklearn carregado: {self.model_file}")
                logger.info(f"✓ Tipo: {self.model_info.get('model_type', 'Unknown')}")
                return
        except Exception as e:
            logger.error(f"Falha ao carregar modelo sklearn: {e}")

        # 3) Fallback final: modelo baseado em regras
        logger.warning(
            "⚠️ Nenhum modelo IA encontrado. Usando modelo baseado em regras."
        )
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
            if self.model_framework == "tf_keras":
                return self._tf_prediction(audio_features)
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

    def _tf_prediction(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Predição usando modelo TF/Keras (espectrograma)."""
        try:
            if tf is None or self.model is None:
                logger.error("TensorFlow/Keras indisponível para predição")
                return self._rule_based_prediction(features)

            audio_path = features.get("audio_path")
            if not audio_path or not os.path.exists(audio_path):
                logger.error("Caminho do áudio não fornecido ou inválido")
                return self._rule_based_prediction(features)

            # Obter input shape do modelo (None, H, W, C)
            try:
                _, H, W, C = self.model.input_shape
            except Exception:
                # Defaults comuns do EfficientNet
                H, W, C = 224, 224, 3

            # Preparar espectrograma log-mel
            import librosa

            target_sr = features.get("sample_rate", 22050)
            y, sr = librosa.load(audio_path, sr=target_sr)

            # Mel-espectrograma
            n_mels = min(128, H)  # limitar mels ao tamanho de altura
            S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, fmax=sr / 2)
            S_db = librosa.power_to_db(S, ref=np.max)

            # Normalização 0..1
            S_min, S_max = float(np.min(S_db)), float(np.max(S_db))
            S_norm = (S_db - S_min) / (S_max - S_min + 1e-8)
            S_norm = S_norm.astype("float32")

            # Para ter (H, W), redimensionamos usando tf.image.resize
            # Primeiro garantir shape (n_mels, T, 1)
            spec = np.expand_dims(S_norm, axis=-1)  # (n_mels, T, 1)
            spec_tf = tf.convert_to_tensor(spec)
            spec_tf = tf.image.resize(spec_tf, size=(H, W), method="bilinear")

            # Ajustar canais
            if C == 3:
                spec_tf = tf.image.grayscale_to_rgb(spec_tf)
            elif C == 1:
                # já é 1 canal
                pass
            else:
                # Tila para C canais caso o modelo espere canais diferentes
                spec_tf = tf.tile(spec_tf, multiples=[1, 1, C])

            # Adicionar batch
            inp = tf.expand_dims(spec_tf, axis=0)  # (1, H, W, C)

            # Predizer
            preds = self.model.predict(inp, verbose=0)
            preds = np.array(preds)

            # Inferir probabilidade de "gunshot".
            # Heurística: se 1 saída -> sigmoide; se >=2 -> assume índice 1 = gunshot.
            if preds.ndim == 2:
                num_classes = preds.shape[1]
                if num_classes == 1:
                    gunshot_prob = float(preds[0, 0])
                else:
                    # Softmax ou logits
                    row = preds[0]
                    # Caso pareça logits, aplica softmax por segurança
                    if not np.all((row >= 0.0) & (row <= 1.0)) or not np.isclose(
                        np.sum(row), 1.0, atol=1e-3
                    ):
                        exp = np.exp(row - np.max(row))
                        row = exp / np.sum(exp)
                    gunshot_prob = float(row[1]) if num_classes > 1 else float(row[0])
            else:
                # Formato inesperado
                gunshot_prob = float(np.squeeze(preds))

            gunshot_detected = gunshot_prob >= 0.5

            # Determinar nível de risco
            if gunshot_prob >= 0.8:
                risk_level = "high"
            elif gunshot_prob >= 0.5:
                risk_level = "medium"
            elif gunshot_prob >= 0.3:
                risk_level = "low"
            else:
                risk_level = "none"

            # Uma detecção sintética no meio da duração para UI
            detections = []
            if gunshot_detected:
                duration = features.get("duration", 0)
                detections.append(
                    {
                        "timestamp": round(float(duration) / 2 if duration else 0.0, 2),
                        "confidence": round(float(gunshot_prob), 2),
                        "type": "gunshot",
                    }
                )

            logger.info(
                f"🎯 Predição Keras: {'TIRO' if gunshot_detected else 'NÃO-TIRO'} (conf: {gunshot_prob:.2%})"
            )

            return {
                "gunshot_detected": bool(gunshot_detected),
                "confidence": round(float(gunshot_prob), 2),
                "probability": round(float(gunshot_prob), 2),
                "risk_level": risk_level,
                "detections": detections,
                "method": "keras_efficientnet",
                "model_type": self.model_info.get("type", "keras"),
            }
        except Exception as e:
            logger.error(f"Erro na predição TF/Keras: {e}")
            return self._rule_based_prediction(features)

    def is_loaded(self) -> bool:
        """Verifica se o modelo está carregado"""
        return self.model is not None

    def get_model_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o modelo"""
        info = {
            **self.model_info,
            "loaded": self.is_loaded(),
            "load_error": self.last_error,
        }
        if self.model_framework == "tf_keras":
            info.update(
                {
                    "model_path": str(self.tf_dir),
                    "framework": "tf.keras",
                }
            )
        elif self.model_framework == "sklearn":
            info.update(
                {
                    "model_path": str(self.model_file),
                    "framework": "sklearn",
                }
            )
        else:
            info.update(
                {
                    "model_path": "<rule_based>",
                    "framework": "rules",
                }
            )
        return info
