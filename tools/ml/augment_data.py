import os
import librosa
import soundfile as sf
import numpy as np
from pathlib import Path


def pitch_shift(y, sr, n_steps):
    return librosa.effects.pitch_shift(y, sr, n_steps=n_steps)


def time_stretch(y, rate):
    return librosa.effects.time_stretch(y, rate)


def add_noise(y, noise_factor=0.005):
    noise = np.random.randn(len(y))
    return y + noise_factor * noise


def augment_file(input_path, output_dir, sr=22050):
    y, _ = librosa.load(input_path, sr=sr)
    base = Path(input_path).stem
    os.makedirs(output_dir, exist_ok=True)

    # pitch shifts
    for i, step in enumerate([-2, 2]):
        y_ps = pitch_shift(y, sr, n_steps=step)
        out = Path(output_dir) / f"{base}_pitch{step}.wav"
        sf.write(out, y_ps, sr)

    # time stretch
    for rate in [0.9, 1.1]:
        y_ts = time_stretch(y, rate=rate)
        out = Path(output_dir) / f"{base}_stretch{rate}.wav"
        sf.write(out, y_ts, sr)

    # add noise
    y_n = add_noise(y, noise_factor=0.005)
    out = Path(output_dir) / f"{base}_noise.wav"
    sf.write(out, y_n, sr)


def augment_directory(input_dir, output_dir, sr=22050, max_files=None):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    files = list(input_dir.glob("**/*.wav"))
    if max_files:
        files = files[:max_files]

    for f in files:
        augment_file(str(f), str(output_dir / f.stem), sr=sr)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Augment audio dataset")
    parser.add_argument("input_dir")
    parser.add_argument("output_dir")
    parser.add_argument("--sr", type=int, default=22050)
    args = parser.parse_args()
    augment_directory(args.input_dir, args.output_dir, sr=args.sr)
