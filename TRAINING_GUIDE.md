# Guia Completo de Treinamento do Modelo de IA

Este guia explica como treinar um modelo de IA para detectar tiros de arma de fogo.

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Coleta de Dados](#coleta-de-dados)
3. [Preparação do Ambiente](#preparação-do-ambiente)
4. [Treinamento do Modelo](#treinamento-do-modelo)
5. [Teste e Validação](#teste-e-validação)
6. [Integração com o Backend](#integração-com-o-backend)
7. [Melhorando o Modelo](#melhorando-o-modelo)

---

## 🎯 Visão Geral

O sistema usa **Machine Learning** para classificar áudios em duas categorias:
- **Tiro de arma de fogo** (classe 1)
- **Não-tiro** (classe 0)

### Tecnologias Utilizadas

- **Librosa**: Extração de features de áudio
- **Scikit-learn**: Treinamento do modelo (Random Forest)
- **NumPy**: Processamento numérico

### Como Funciona

1. **Extração de Features**: O áudio é convertido em características numéricas (MFCCs, spectral features, etc.)
2. **Treinamento**: O modelo aprende padrões que diferenciam tiros de outros sons
3. **Predição**: Novos áudios são classificados com base nos padrões aprendidos

---

## 📊 Coleta de Dados

### Onde Conseguir Dados

#### 1. Datasets Públicos

**UrbanSound8K** (Recomendado)
- URL: https://urbansounddataset.weebly.com/urbansound8k.html
- Contém: 8732 sons urbanos incluindo tiros
- Formato: WAV, 4 segundos cada
- Licença: Uso acadêmico

**Freesound.org**
- URL: https://freesound.org/search/?q=gunshot
- Contém: Milhares de sons de tiros
- Formato: Vários (WAV, MP3, etc.)
- Licença: Creative Commons (verificar cada áudio)

**AudioSet (Google)**
- URL: https://research.google.com/audioset/
- Contém: Milhões de áudios rotulados
- Categoria: "Gunshot, gunfire"
- Formato: Links para YouTube

**ESC-50 Dataset**
- URL: https://github.com/karolpiczak/ESC-50
- Contém: 2000 sons ambientais
- Inclui: Tiros e sons similares

#### 2. Gravação Própria

Se você tiver acesso seguro a um campo de tiro:
- Grave com microfone de qualidade
- Diferentes distâncias (perto, médio, longe)
- Diferentes tipos de armas
- Diferentes ambientes (aberto, fechado)

⚠️ **IMPORTANTE**: Sempre siga as leis locais e medidas de segurança!

### Dados de Não-Tiros (Essencial!)

Para evitar falsos positivos, colete sons similares:

- **Fogos de artifício** (muito similar a tiros)
- **Batidas de porta** (som impulsivo)
- **Estouro de balões**
- **Trovões**
- **Batidas de martelo**
- **Sons de construção**
- **Tráfego urbano**
- **Latidos de cachorro**

### Quantidade Recomendada

| Categoria | Mínimo | Recomendado | Ideal |
|-----------|--------|-------------|-------|
| Tiros | 50 | 200 | 500+ |
| Não-tiros | 50 | 200 | 500+ |

**Regra de ouro**: Quanto mais dados, melhor o modelo!

---

## 🛠️ Preparação do Ambiente

### 1. Estrutura de Diretórios

\`\`\`bash
# Execute o script de setup
python ml/download_dataset.py
\`\`\`

Isso criará:
\`\`\`
data/
├── gunshots/          # Coloque áudios de tiros aqui
├── non_gunshots/      # Coloque áudios de não-tiros aqui
├── raw/               # Dados brutos (opcional)
└── test/              # Áudios para teste (opcional)

models/                # Modelos treinados serão salvos aqui
\`\`\`

### 2. Organize os Dados

\`\`\`bash
# Exemplo de organização
data/gunshots/
├── pistol_shot_01.wav
├── rifle_shot_01.wav
├── shotgun_01.wav
└── ...

data/non_gunshots/
├── firework_01.wav
├── door_slam_01.wav
├── thunder_01.wav
└── ...
\`\`\`

### 3. Formato dos Áudios

- **Formato**: WAV (preferencial) ou MP3
- **Duração**: 1-5 segundos (ideal: 2-3 segundos)
- **Sample Rate**: Qualquer (será convertido para 22050 Hz)
- **Canais**: Mono ou Stereo (será convertido para mono)

---

## 🚀 Treinamento do Modelo

### Passo 1: Verificar os Dados

\`\`\`bash
# Liste os arquivos
ls data/gunshots/
ls data/non_gunshots/
\`\`\`

### Passo 2: Executar o Treinamento

\`\`\`bash
python ml/train_gunshot_detector.py
\`\`\`

### O que Acontece Durante o Treinamento

1. **Carregamento**: Lê todos os arquivos de áudio
2. **Extração de Features**: Converte áudio em números
3. **Divisão**: 80% treino, 20% teste
4. **Treinamento**: Random Forest aprende os padrões
5. **Validação**: Testa a acurácia
6. **Salvamento**: Modelo salvo em `models/`

### Interpretando os Resultados

\`\`\`
RESULTADOS DO TREINAMENTO
==================================================

Acurácia no treino: 0.9850
Acurácia no teste: 0.9200

Cross-validation (5-fold):
  Média: 0.9100
  Desvio padrão: 0.0250

Relatório de Classificação:
              precision    recall  f1-score   support

   Não-tiro       0.91      0.93      0.92        40
       Tiro       0.93      0.91      0.92        40

    accuracy                           0.92        80
\`\`\`

**O que significa:**

- **Acurácia**: % de predições corretas
  - Treino: 98.5% (muito bom!)
  - Teste: 92% (bom, mas menor que treino é normal)

- **Precision**: Quando prevê "tiro", quantos % estão corretos
  - 93% = de 100 alertas de tiro, 93 são reais

- **Recall**: De todos os tiros reais, quantos % foram detectados
  - 91% = de 100 tiros reais, 91 foram detectados

- **F1-score**: Média harmônica de precision e recall
  - 92% = bom equilíbrio

### Matriz de Confusão

\`\`\`
[[37  3]     Verdadeiros Negativos: 37 (não-tiros corretos)
 [ 4 36]]    Falsos Positivos: 3 (alertou tiro, mas não era)
             Falsos Negativos: 4 (não alertou, mas era tiro)
             Verdadeiros Positivos: 36 (tiros detectados corretamente)
\`\`\`

---

## 🧪 Teste e Validação

### Testar um Único Áudio

\`\`\`bash
python ml/test_model.py caminho/para/audio.wav
\`\`\`

Saída:
\`\`\`
Testando: audio.wav
==================================================
Extraindo features...

RESULTADOS:
  Predição: 🔫 TIRO DETECTADO
  Confiança (não-tiro): 15.23%
  Confiança (tiro): 84.77%
==================================================
\`\`\`

### Teste em Batch

\`\`\`bash
python ml/test_model.py --batch data/test/
\`\`\`

### Validação Manual

1. Teste com áudios que você SABE que são tiros
2. Teste com áudios que você SABE que NÃO são tiros
3. Teste com áudios ambíguos (fogos de artifício, etc.)

---

## 🔌 Integração com o Backend

### Passo 1: Copiar o Modelo

O modelo já está configurado para ser usado pelo backend FastAPI.

\`\`\`bash
# O modelo está em:
models/gunshot_detector.pkl
models/model_metadata.json
\`\`\`

### Passo 2: Atualizar o Backend

O arquivo `backend/model_loader.py` já está configurado para carregar seu modelo treinado.

### Passo 3: Testar a Integração

\`\`\`bash
# Inicie o backend
docker-compose up backend

# Em outro terminal, teste a API
curl -X POST http://localhost:8000/analyze \
  -F "file=@test_audio.wav"
\`\`\`

### Passo 4: Testar pelo Frontend

1. Acesse http://localhost:3000
2. Faça upload de um áudio
3. Clique em "Analisar Áudio"
4. Veja os resultados com seu modelo treinado!

---

## 📈 Melhorando o Modelo

### Se a Acurácia Está Baixa (<80%)

1. **Adicione mais dados**
   - Objetivo: 200+ amostras de cada classe
   - Varie os tipos de tiros e ambientes

2. **Balance as classes**
   - Mesma quantidade de tiros e não-tiros
   - Use data augmentation se necessário

3. **Limpe os dados**
   - Remova áudios com ruído excessivo
   - Remova áudios mal rotulados

### Se Há Muitos Falsos Positivos

Falso positivo = alerta de tiro quando não é tiro

**Solução**: Adicione mais exemplos de sons similares aos não-tiros:
- Mais fogos de artifício
- Mais batidas de porta
- Mais sons impulsivos

### Se Há Muitos Falsos Negativos

Falso negativo = não detecta tiro quando é tiro

**Solução**: Adicione mais variedade de tiros:
- Diferentes tipos de armas
- Diferentes distâncias
- Diferentes ambientes (eco, aberto, fechado)

### Técnicas Avançadas

#### 1. Data Augmentation

Aumente artificialmente seu dataset:

\`\`\`python
# Adicione ao train_gunshot_detector.py
import librosa

def augment_audio(y, sr):
    # Adiciona ruído
    noise = np.random.randn(len(y))
    y_noise = y + 0.005 * noise
    
    # Muda o pitch
    y_pitch = librosa.effects.pitch_shift(y, sr=sr, n_steps=2)
    
    # Muda a velocidade
    y_speed = librosa.effects.time_stretch(y, rate=1.1)
    
    return [y_noise, y_pitch, y_speed]
\`\`\`

#### 2. Ajuste de Hiperparâmetros

Modifique em `train_gunshot_detector.py`:

\`\`\`python
self.model = RandomForestClassifier(
    n_estimators=300,      # Mais árvores (padrão: 200)
    max_depth=25,          # Árvores mais profundas (padrão: 20)
    min_samples_split=3,   # Menos amostras para split (padrão: 5)
    class_weight='balanced' # Balance classes automaticamente
)
\`\`\`

#### 3. Modelos Alternativos

Experimente outros algoritmos:

\`\`\`python
# SVM (bom para dados pequenos)
from sklearn.svm import SVC
model = SVC(kernel='rbf', probability=True)

# Gradient Boosting (geralmente mais preciso)
from sklearn.ensemble import GradientBoostingClassifier
model = GradientBoostingClassifier(n_estimators=200)

# Neural Network (para datasets grandes)
from sklearn.neural_network import MLPClassifier
model = MLPClassifier(hidden_layer_sizes=(100, 50))
\`\`\`

---

## 🎓 Recursos Adicionais

### Tutoriais

- [Librosa Tutorial](https://librosa.org/doc/latest/tutorial.html)
- [Audio Classification with ML](https://towardsdatascience.com/audio-classification-using-machine-learning-5f8e8c3c6f0c)
- [Random Forest Explained](https://www.datacamp.com/tutorial/random-forests-classifier-python)

### Papers Acadêmicos

- "Gunshot Detection Systems: A Survey" (IEEE)
- "Urban Sound Classification using Deep Learning"

### Comunidades

- r/MachineLearning (Reddit)
- Kaggle Competitions (Audio Classification)
- Stack Overflow (tag: audio-processing)

---

## ❓ FAQ

**P: Quanto tempo leva o treinamento?**
R: Com 200 amostras: ~2-5 minutos. Com 1000+: ~10-30 minutos.

**P: Preciso de GPU?**
R: Não! Random Forest roda bem em CPU.

**P: Posso usar MP3 ao invés de WAV?**
R: Sim, librosa converte automaticamente.

**P: O modelo funciona em tempo real?**
R: Sim! A predição leva ~100-300ms por áudio.

**P: Como atualizo o modelo sem perder o anterior?**
R: Renomeie o modelo antigo antes de treinar:
\`\`\`bash
mv models/gunshot_detector.pkl models/gunshot_detector_v1.pkl
python ml/train_gunshot_detector.py
\`\`\`

---

## 📞 Suporte

Se tiver problemas:

1. Verifique os logs de erro
2. Confirme que os diretórios estão corretos
3. Teste com poucos arquivos primeiro
4. Consulte a documentação do Librosa

**Boa sorte com o treinamento! 🎯**
\`\`\`

```python file="" isHidden
