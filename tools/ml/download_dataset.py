"""
Script para baixar datasets públicos de tiros e sons urbanos
"""

import os
import urllib.request
import zipfile
from pathlib import Path


def download_file(url, destination):
    """
    Baixa um arquivo da internet
    """
    print(f"Baixando: {url}")
    urllib.request.urlretrieve(url, destination)
    print(f"✓ Salvo em: {destination}")


def extract_zip(zip_path, extract_to):
    """
    Extrai um arquivo ZIP
    """
    print(f"Extraindo: {zip_path}")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"✓ Extraído para: {extract_to}")


def setup_directories():
    """
    Cria a estrutura de diretórios para os dados
    """
    dirs = ["data/gunshots", "data/non_gunshots", "data/raw", "models"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"✓ Diretório criado: {d}")


def main():
    print("=" * 50)
    print("SETUP DE DATASET PARA DETECÇÃO DE TIROS")
    print("=" * 50 + "\n")

    setup_directories()

    print("\n" + "=" * 50)
    print("DATASETS RECOMENDADOS")
    print("=" * 50)

    print(
        """
    Para treinar o modelo, você precisa de áudios de:
    
    1. TIROS DE ARMA DE FOGO:
       - Freesound.org: https://freesound.org/search/?q=gunshot
       - AudioSet (Google): https://research.google.com/audioset/
       - UrbanSound8K: https://urbansounddataset.weebly.com/urbansound8k.html
       
    2. SONS NÃO-TIROS (para evitar falsos positivos):
       - Explosões de fogos de artifício
       - Batidas de porta
       - Estouro de balões
       - Trovões
       - Sons urbanos diversos
    
    INSTRUÇÕES:
    
    1. Baixe os áudios dos sites acima
    2. Coloque os áudios de tiros em: data/gunshots/
    3. Coloque os áudios de não-tiros em: data/non_gunshots/
    4. Execute: python ml/train_gunshot_detector.py
    
    DICA: Quanto mais dados, melhor o modelo!
    Recomendado: pelo menos 100-200 amostras de cada classe.
    """
    )

    print("\n✓ Setup concluído!")
    print("\nPróximos passos:")
    print("  1. Baixe os datasets manualmente")
    print("  2. Organize os arquivos nas pastas corretas")
    print("  3. Execute o treinamento")


if __name__ == "__main__":
    main()
