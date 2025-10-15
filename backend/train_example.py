"""
Script de exemplo para treinar um modelo de detecção de tiros

Este é um template que você pode adaptar com seus próprios dados
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
import pickle
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_training_data():
    """
    Carrega dados de treinamento
    
    VOCÊ PRECISA IMPLEMENTAR ESTA FUNÇÃO com seus dados reais
    
    Retorna:
        X: array de features (n_samples, n_features)
        y: array de labels (n_samples,) - 0 = não é tiro, 1 = é tiro
    """
    
    # EXEMPLO - Substitua com seus dados reais
    # Cada linha é um áudio, cada coluna é uma feature
    
    # Features que o audio_processor.py extrai:
    # [energy, zero_crossing_rate, spectral_centroid, spectral_rolloff, 
    #  peak_frequency, mfcc_1, mfcc_2, ..., mfcc_13]
    
    # Exemplo de dados sintéticos (SUBSTITUA COM DADOS REAIS)
    n_samples = 1000
    n_features = 18  # 5 features básicas + 13 MFCCs
    
    # Simular dados de tiros (alta energia, frequências características)
    gunshots = np.random.randn(n_samples // 2, n_features)
    gunshots[:, 0] = np.random.uniform(0.6, 1.0, n_samples // 2)  # Alta energia
    gunshots[:, 4] = np.random.uniform(1000, 4000, n_samples // 2)  # Freq característica
    
    # Simular dados de não-tiros (baixa energia, frequências variadas)
    non_gunshots = np.random.randn(n_samples // 2, n_features)
    non_gunshots[:, 0] = np.random.uniform(0.0, 0.5, n_samples // 2)  # Baixa energia
    non_gunshots[:, 4] = np.random.uniform(0, 10000, n_samples // 2)  # Freq variada
    
    X = np.vstack([gunshots, non_gunshots])
    y = np.hstack([np.ones(n_samples // 2), np.zeros(n_samples // 2)])
    
    # Embaralhar
    indices = np.random.permutation(len(X))
    X = X[indices]
    y = y[indices]
    
    logger.warning("ATENÇÃO: Usando dados sintéticos! Substitua com dados reais.")
    
    return X, y

def train_model():
    """Treina o modelo de detecção de tiros"""
    
    logger.info("Carregando dados de treinamento...")
    X, y = load_training_data()
    
    logger.info(f"Dataset: {len(X)} amostras, {X.shape[1]} features")
    logger.info(f"Classes: {np.sum(y == 1)} tiros, {np.sum(y == 0)} não-tiros")
    
    # Dividir em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    logger.info("Treinando modelo Random Forest...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    
    # Treinar
    model.fit(X_train, y_train)
    
    # Avaliar
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    logger.info(f"Acurácia treino: {train_score:.3f}")
    logger.info(f"Acurácia teste: {test_score:.3f}")
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    logger.info(f"Cross-validation: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
    
    # Predições no conjunto de teste
    y_pred = model.predict(X_test)
    
    # Relatório detalhado
    logger.info("\nRelatório de Classificação:")
    print(classification_report(y_test, y_pred, target_names=['Não-tiro', 'Tiro']))
    
    logger.info("\nMatriz de Confusão:")
    print(confusion_matrix(y_test, y_pred))
    
    # Importância das features
    feature_names = [
        'energy', 'zero_crossing_rate', 'spectral_centroid', 
        'spectral_rolloff', 'peak_frequency'
    ] + [f'mfcc_{i}' for i in range(1, 14)]
    
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    logger.info("\nImportância das Features:")
    for i in range(min(10, len(feature_names))):
        idx = indices[i]
        logger.info(f"{feature_names[idx]}: {importances[idx]:.3f}")
    
    return model, test_score

def save_model(model, accuracy):
    """Salva o modelo treinado"""
    
    models_dir = Path("/app/models")
    models_dir.mkdir(exist_ok=True)
    
    # Salvar modelo
    model_path = models_dir / "gunshot_model.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    logger.info(f"Modelo salvo em: {model_path}")
    
    # Salvar configuração
    config = {
        "name": "Gunshot Detection Model",
        "version": "1.0.0",
        "type": "random_forest",
        "description": "Modelo Random Forest para detecção de tiros em áudio",
        "trained_date": "2025-10-08",
        "accuracy": float(accuracy),
        "n_estimators": 100,
        "features": [
            "energy", "zero_crossing_rate", "spectral_centroid",
            "spectral_rolloff", "peak_frequency", "mfccs (13)"
        ]
    }
    
    config_path = models_dir / "model_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    logger.info(f"Configuração salva em: {config_path}")

if __name__ == "__main__":
    logger.info("=== Treinamento de Modelo de Detecção de Tiros ===")
    
    # Treinar
    model, accuracy = train_model()
    
    # Salvar
    save_model(model, accuracy)
    
    logger.info("\n✓ Treinamento concluído!")
    logger.info("Para usar o modelo, reinicie o backend:")
    logger.info("  docker-compose restart backend")
