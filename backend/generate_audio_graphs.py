import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

GRAPHS_DIR = Path("graphs")
GRAPHS_DIR.mkdir(exist_ok=True)


def generate_audio_graphs(audio_path: str):
    """
    Gera e salva três gráficos (FFT, MFCC e Log-Mel) a partir de um arquivo de áudio.
    Retorna os caminhos dos arquivos gerados.
    """
    try:
        # Carrega o áudio
        y, sr = librosa.load(audio_path, sr=None)

        # ----- (a) FFT -----
        plt.figure(figsize=(6, 3))
        D = np.abs(librosa.stft(y))
        librosa.display.specshow(
            librosa.amplitude_to_db(D, ref=np.max),
            sr=sr,
            x_axis="time",
            y_axis="log",
            cmap="magma",
        )
        plt.title("Extração de características com FFT")
        fft_path = GRAPHS_DIR / f"{Path(audio_path).stem}_fft.png"
        plt.savefig(fft_path, bbox_inches="tight")
        plt.close()

        # ----- (b) MFCC -----
        plt.figure(figsize=(6, 3))
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        librosa.display.specshow(mfccs, x_axis="time", cmap="RdBu_r")
        plt.title("Extração de características com MFCC")
        mfcc_path = GRAPHS_DIR / f"{Path(audio_path).stem}_mfcc.png"
        plt.savefig(mfcc_path, bbox_inches="tight")
        plt.close()

        # ----- (c) Log-Mel -----
        plt.figure(figsize=(6, 3))
        S = librosa.feature.melspectrogram(y=y, sr=sr)
        librosa.display.specshow(
            librosa.power_to_db(S, ref=np.max),
            sr=sr,
            x_axis="time",
            y_axis="mel",
            cmap="magma",
        )
        plt.title("Extração de características com LogMel")
        logmel_path = GRAPHS_DIR / f"{Path(audio_path).stem}_logmel.png"
        plt.savefig(logmel_path, bbox_inches="tight")
        plt.close()

        return {
            "fft": str(fft_path),
            "mfcc": str(mfcc_path),
            "logmel": str(logmel_path),
        }

    except Exception as e:
        raise RuntimeError(f"Erro ao gerar gráficos: {e}")
