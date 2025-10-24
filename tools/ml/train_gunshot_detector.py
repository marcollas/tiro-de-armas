import os
import numpy as np
import librosa
import pickle
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import json
from pathlib import Path


class GunshotDetectorTrainer:
    """
    Treinador de modelo para detecção de tiros de arma de fogo
    """

    def __init__(self, sample_rate=22050, n_mfcc=40, n_fft=2048, hop_length=512):
        self.sample_rate = sample_rate
        self.n_mfcc = n_mfcc
        self.n_fft = n_fft
        self.hop_length = hop_length
        self.model = None
        self.feature_scaler = None

    def extract_features(self, audio_path):
        """
        Extrai features de áudio para treinamento

        Features extraídas:
        - MFCCs (Mel-frequency cepstral coefficients)
        - Spectral Centroid
        - Spectral Rolloff
        - Zero Crossing Rate
        - Chroma Features
        - Spectral Contrast
        """
        try:
            # Carrega o áudio
            y, sr = librosa.load(audio_path, sr=self.sample_rate, duration=3.0)

            # Normaliza o áudio
            y = librosa.util.normalize(y)

            features = []

            # MFCCs - características importantes para classificação de áudio
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=self.n_mfcc)
            features.extend(
                [
                    np.mean(mfccs, axis=1),
                    np.std(mfccs, axis=1),
                    np.max(mfccs, axis=1),
                    np.min(mfccs, axis=1),
                ]
            )

            # Spectral Centroid - centro de massa do espectro
            spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
            features.extend(
                [
                    np.mean(spectral_centroid),
                    np.std(spectral_centroid),
                    np.max(spectral_centroid),
                ]
            )

            # Spectral Rolloff - frequência abaixo da qual está 85% da energia
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
            features.extend([np.mean(spectral_rolloff), np.std(spectral_rolloff)])

            # Zero Crossing Rate - taxa de mudança de sinal
            zcr = librosa.feature.zero_crossing_rate(y)
            features.extend([np.mean(zcr), np.std(zcr)])

            # Chroma Features - representação de classes de pitch
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            features.extend([np.mean(chroma, axis=1), np.std(chroma, axis=1)])

            # Spectral Contrast - diferença entre picos e vales no espectro
            contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
            features.extend([np.mean(contrast, axis=1), np.std(contrast, axis=1)])

            # RMS Energy - energia do sinal
            rms = librosa.feature.rms(y=y)
            features.extend([np.mean(rms), np.std(rms), np.max(rms)])

            # Flatten todas as features
            feature_vector = np.concatenate([np.array(f).flatten() for f in features])

            return feature_vector

        except Exception as e:
            print(f"Erro ao extrair features de {audio_path}: {e}")
            return None

    def prepare_dataset(self, gunshot_dir, non_gunshot_dir):
        """
        Prepara o dataset a partir de diretórios de áudio

        Args:
            gunshot_dir: Diretório com áudios de tiros
            non_gunshot_dir: Diretório com áudios de não-tiros
        """
        X = []
        y = []

        print("Processando áudios de tiros...")
        gunshot_path = Path(gunshot_dir)
        for audio_file in gunshot_path.glob("**/*.wav"):
            features = self.extract_features(str(audio_file))
            if features is not None:
                X.append(features)
                y.append(1)  # 1 = tiro
                print(f"✓ Processado: {audio_file.name}")

        print(f"\nProcessando áudios de não-tiros...")
        non_gunshot_path = Path(non_gunshot_dir)
        for audio_file in non_gunshot_path.glob("**/*.wav"):
            features = self.extract_features(str(audio_file))
            if features is not None:
                X.append(features)
                y.append(0)  # 0 = não-tiro
                print(f"✓ Processado: {audio_file.name}")

        X = np.array(X)
        y = np.array(y)

        print(f"\n{'='*50}")
        print(f"Dataset preparado:")
        print(f"  Total de amostras: {len(X)}")
        print(f"  Tiros: {np.sum(y == 1)}")
        print(f"  Não-tiros: {np.sum(y == 0)}")
        print(f"  Dimensão das features: {X.shape[1]}")
        print(f"{'='*50}\n")

        return X, y

    def train(self, X, y, test_size=0.2, random_state=42):
        """
        Treina o modelo de detecção
        """
        # Divide em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )

        # Escalar features (melhora muitos modelos baseados em árvore e obrigatorio para alguns modelos)
        self.feature_scaler = StandardScaler()
        X_train = self.feature_scaler.fit_transform(X_train)
        X_test = self.feature_scaler.transform(X_test)

        print("Treinando modelo Random Forest...")

        # Random Forest é robusto e funciona bem para classificação de áudio
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=random_state,
            n_jobs=-1,
            verbose=1,
        )

        # Treina o modelo
        self.model.fit(X_train, y_train)

        # Avalia o modelo
        print("\n" + "=" * 50)
        print("RESULTADOS DO TREINAMENTO")
        print("=" * 50)

        # Acurácia no conjunto de treino
        train_score = self.model.score(X_train, y_train)
        print(f"\nAcurácia no treino: {train_score:.4f}")

        # Acurácia no conjunto de teste
        test_score = self.model.score(X_test, y_test)
        print(f"Acurácia no teste: {test_score:.4f}")

        # Cross-validation
        cv_scores = cross_val_score(self.model, X_train, y_train, cv=5)
        print(f"\nCross-validation (5-fold):")
        print(f"  Média: {cv_scores.mean():.4f}")
        print(f"  Desvio padrão: {cv_scores.std():.4f}")

        # Predições no conjunto de teste
        y_pred = self.model.predict(X_test)

        # Relatório de classificação
        print("\nRelatório de Classificação:")
        print(classification_report(y_test, y_pred, target_names=["Não-tiro", "Tiro"]))

        # Matriz de confusão
        print("\nMatriz de Confusão:")
        cm = confusion_matrix(y_test, y_pred)
        print(cm)
        print(f"\nVerdadeiros Negativos: {cm[0][0]}")
        print(f"Falsos Positivos: {cm[0][1]}")
        print(f"Falsos Negativos: {cm[1][0]}")
        print(f"Verdadeiros Positivos: {cm[1][1]}")

        # Feature importance
        feature_importance = self.model.feature_importances_
        print(f"\nTop 10 features mais importantes:")
        top_indices = np.argsort(feature_importance)[-10:][::-1]
        for i, idx in enumerate(top_indices, 1):
            print(f"  {i}. Feature {idx}: {feature_importance[idx]:.4f}")

        print("=" * 50 + "\n")

        # Salvar scaler para uso durante inference
        try:
            os.makedirs("models", exist_ok=True)
            joblib.dump(self.feature_scaler, "models/scaler.joblib")
            print(f"\u2713 Scaler salvo em: models/scaler.joblib")
        except Exception as e:
            print(f"Erro ao salvar scaler: {e}")

        return {
            "train_score": train_score,
            "test_score": test_score,
            "cv_mean": cv_scores.mean(),
            "cv_std": cv_scores.std(),
        }

    def save_model(
        self,
        model_path="models/gunshot_detector.pkl",
        metadata_path="models/model_metadata.json",
    ):
        """
        Salva o modelo treinado
        """
        os.makedirs(os.path.dirname(model_path), exist_ok=True)

        # Salva o modelo
        with open(model_path, "wb") as f:
            pickle.dump(self.model, f)
        # Também salvar o scaler se existir
        try:
            if self.feature_scaler is not None:
                joblib.dump(
                    self.feature_scaler,
                    os.path.join(os.path.dirname(model_path), "scaler.joblib"),
                )
        except Exception:
            pass

        # Salva metadados
        metadata = {
            "sample_rate": self.sample_rate,
            "n_mfcc": self.n_mfcc,
            "n_fft": self.n_fft,
            "hop_length": self.hop_length,
            "model_type": "RandomForestClassifier",
            "n_estimators": self.model.n_estimators,
            "feature_dim": self.model.n_features_in_,
        }

        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)

        print(f"✓ Modelo salvo em: {model_path}")
        print(f"✓ Metadados salvos em: {metadata_path}")

    def load_model(
        self,
        model_path="models/gunshot_detector.pkl",
        metadata_path="models/model_metadata.json",
    ):
        """
        Carrega um modelo treinado
        """
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

        with open(metadata_path, "r") as f:
            metadata = json.load(f)
            self.sample_rate = metadata["sample_rate"]
            self.n_mfcc = metadata["n_mfcc"]
            self.n_fft = metadata["n_fft"]
            self.hop_length = metadata["hop_length"]

        print(f"✓ Modelo carregado de: {model_path}")
        return metadata


def main():
    """
    Exemplo de uso do treinador
    """
    print("=" * 50)
    print("TREINADOR DE DETECTOR DE TIROS")
    print("=" * 50 + "\n")

    # Inicializa o treinador
    trainer = GunshotDetectorTrainer()
    # Diretórios com os dados
    gunshot_dir = "data/gunshots"
    non_gunshot_dir = "data/non_gunshots"

    # Se data/ não estiver acessível, tentar augmented/ como fallback
    if not os.path.exists(gunshot_dir) or not os.path.exists(non_gunshot_dir):
        alt_gun = "augmented/gunshots"
        alt_non = "augmented/non_gunshots"
        if os.path.exists(alt_gun) and os.path.exists(alt_non):
            print(
                "ℹ️  data/ não encontrado ou inacessível; usando 'augmented/' como fallback."
            )
            gunshot_dir = alt_gun
            non_gunshot_dir = alt_non
        else:
            print("⚠️  ATENÇÃO: Diretórios de dados não encontrados!")
            print(f"\nCrie os seguintes diretórios e adicione arquivos .wav:")
            print(f"  - data/gunshots/  (áudios de tiros)")
            print(f"  - data/non_gunshots/  (áudios de não-tiros)")
            print(
                "\nOu coloque os arquivos em 'augmented/gunshots' e 'augmented/non_gunshots' e tente novamente."
            )
            print("\nVeja TRAINING_GUIDE.md para mais informações sobre datasets.")
            return

    # Prepara o dataset
    X, y = trainer.prepare_dataset(gunshot_dir, non_gunshot_dir)

    if len(X) < 10:
        print("⚠️  Dataset muito pequeno! Adicione mais amostras.")
        print("   Recomendado: pelo menos 100 amostras de cada classe.")
        return

    # Treina o modelo
    results = trainer.train(X, y)

    # Salva o modelo
    trainer.save_model()

    print("\n✓ Treinamento concluído com sucesso!")
    print("\nPróximos passos:")
    print("  1. Teste o modelo com novos áudios")
    print("  2. Se a acurácia for baixa, adicione mais dados")
    print("  3. Integre o modelo no backend FastAPI")


if __name__ == "__main__":
    main()
