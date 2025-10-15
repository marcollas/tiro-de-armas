import librosa
import numpy as np
import soundfile as sf
from pathlib import Path
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AudioProcessor:
    """
    Processa arquivos de áudio e extrai características
    """
    
    def __init__(self, sample_rate: int = 22050):
        self.sample_rate = sample_rate
    
    def extract_features(self, audio_path: str) -> Dict[str, Any]:
        """
        Extrai características do áudio para análise
        """
        try:
            # Carregar áudio
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Informações básicas
            duration = librosa.get_duration(y=y, sr=sr)
            
            # Características espectrais
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
            
            # Zero crossing rate (útil para detectar transientes)
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            
            # MFCCs (Mel-frequency cepstral coefficients)
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            
            # Energia do sinal
            rms = librosa.feature.rms(y=y)[0]
            
            # Transformada de Fourier para análise de frequência
            fft = np.fft.fft(y)
            magnitude = np.abs(fft)
            frequency = np.linspace(0, sr, len(magnitude))
            
            # Encontrar frequência dominante
            peak_freq_idx = np.argmax(magnitude[:len(magnitude)//2])
            peak_frequency = frequency[peak_freq_idx]
            
            # Onset detection (detecção de eventos súbitos)
            onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
            onset_times = librosa.frames_to_time(onset_frames, sr=sr)
            
            features = {
                "duration": float(duration),
                "sample_rate": int(sr),
                "channels": 1,
                "energy": float(np.mean(rms)),
                "peak_frequency": float(peak_frequency),
                "spectral_centroid": float(np.mean(spectral_centroids)),
                "spectral_rolloff": float(np.mean(spectral_rolloff)),
                "zero_crossing_rate": float(np.mean(zcr)),
                "mfccs": [float(x) for x in np.mean(mfccs, axis=1)],
                "onset_count": len(onset_times),
                "onset_times": [float(t) for t in onset_times[:10]],  # Primeiros 10
                "audio_path": audio_path  # Adicionar caminho do áudio para o modelo ML usar
            }
            
            logger.info(f"Features extraídas: duration={duration:.2f}s, energy={features['energy']:.3f}")
            
            return features
            
        except Exception as e:
            logger.error(f"Erro ao extrair features: {e}")
            raise
