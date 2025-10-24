import sys
import numpy as np
from train_gunshot_detector import GunshotDetectorTrainer


def test_single_audio(audio_path, model_path="models/gunshot_detector.pkl"):
    """
    Testa o modelo com um único arquivo de áudio
    """
    print(f"\nTestando: {audio_path}")
    print("=" * 50)

    # Carrega o modelo
    trainer = GunshotDetectorTrainer()
    metadata = trainer.load_model(model_path)

    # Extrai features
    print("Extraindo features...")
    features = trainer.extract_features(audio_path)

    if features is None:
        print("❌ Erro ao processar o áudio")
        return

    # Faz a predição
    features = features.reshape(1, -1)
    prediction = trainer.model.predict(features)[0]
    probability = trainer.model.predict_proba(features)[0]

    # Mostra resultados
    print("\nRESULTADOS:")
    print(f"  Predição: {'🔫 TIRO DETECTADO' if prediction == 1 else '✓ Não é tiro'}")
    print(f"  Confiança (não-tiro): {probability[0]:.2%}")
    print(f"  Confiança (tiro): {probability[1]:.2%}")
    print("=" * 50)

    return prediction, probability


def batch_test(test_dir, model_path="models/gunshot_detector.pkl"):
    """
    Testa o modelo com múltiplos arquivos
    """
    from pathlib import Path

    print(f"\nTestando todos os áudios em: {test_dir}")
    print("=" * 50 + "\n")

    trainer = GunshotDetectorTrainer()
    trainer.load_model(model_path)

    test_path = Path(test_dir)
    results = []

    for audio_file in test_path.glob("**/*.wav"):
        features = trainer.extract_features(str(audio_file))
        if features is not None:
            features = features.reshape(1, -1)
            prediction = trainer.model.predict(features)[0]
            probability = trainer.model.predict_proba(features)[0]

            results.append(
                {
                    "file": audio_file.name,
                    "prediction": prediction,
                    "confidence": probability[1],
                }
            )

            status = "🔫 TIRO" if prediction == 1 else "✓ Não-tiro"
            print(f"{status} - {audio_file.name} (confiança: {probability[1]:.2%})")

    print("\n" + "=" * 50)
    print(f"Total testado: {len(results)}")
    print(f"Tiros detectados: {sum(r['prediction'] == 1 for r in results)}")
    print(f"Não-tiros: {sum(r['prediction'] == 0 for r in results)}")
    print("=" * 50)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python ml/test_model.py <arquivo.wav>")
        print("  python ml/test_model.py --batch <diretorio>")
        sys.exit(1)

    if sys.argv[1] == "--batch":
        if len(sys.argv) < 3:
            print("Especifique o diretório para teste em batch")
            sys.exit(1)
        batch_test(sys.argv[2])
    else:
        test_single_audio(sys.argv[1])
