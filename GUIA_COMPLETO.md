# Guia Completo - Sistema de Detecção de Tiros com IA

## Arquitetura do Sistema

O sistema agora usa uma arquitetura de microserviços:

\`\`\`
┌─────────────────┐         ┌──────────────────┐
│   Frontend      │────────▶│   Backend API    │
│   Next.js       │         │   FastAPI        │
│   (Port 3000)   │◀────────│   (Port 8000)    │
└─────────────────┘         └──────────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │  Modelo de IA    │
                            │  (Scikit-learn)  │
                            └──────────────────┘
\`\`\`

## Como Rodar a Aplicação

### Pré-requisitos
- Docker e Docker Compose instalados
- Nenhuma outra dependência necessária

### Iniciar a Aplicação

\`\`\`bash
# Clone ou baixe o projeto
cd gunshot-detector

# Inicie todos os serviços
docker-compose up --build
\`\`\`

Aguarde alguns minutos na primeira execução (download de imagens e build).

### Acessar a Aplicação

- **Frontend**: http://localhost:3000
- **API Backend**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/docs

## Estrutura do Projeto

\`\`\`
gunshot-detector/
├── app/                          # Frontend Next.js
│   ├── api/
│   │   └── analyze-audio/
│   │       └── route.ts         # API route que chama FastAPI
│   └── page.tsx                 # Página principal
├── backend/                      # Microserviço FastAPI
│   ├── main.py                  # API FastAPI principal
│   ├── model_loader.py          # Carregador de modelos de IA
│   ├── audio_processor.py       # Processamento de áudio
│   └── requirements.txt         # Dependências Python
├── components/                   # Componentes React
├── docker-compose.yml           # Orquestração de containers
├── Dockerfile                   # Build do frontend
└── Dockerfile.backend           # Build do backend
\`\`\`

## Endpoints da API

### 1. Análise de Áudio
\`\`\`bash
POST /api/analyze
Content-Type: multipart/form-data

# Exemplo com curl
curl -X POST http://localhost:8000/api/analyze \
  -F "file=@audio.wav"
\`\`\`

**Resposta:**
\`\`\`json
{
  "success": true,
  "filename": "audio.wav",
  "analysis": {
    "gunshot_detected": true,
    "confidence": 0.85,
    "probability": 0.85,
    "risk_level": "high",
    "timestamp": "2025-10-08T22:52:57"
  },
  "audio_features": {
    "duration": 3.5,
    "sample_rate": 22050,
    "energy": 0.72,
    "peak_frequency": 2500
  },
  "detections": [
    {
      "timestamp": 1.2,
      "confidence": 0.87,
      "type": "gunshot"
    }
  ]
}
\`\`\`

### 2. Informações do Modelo
\`\`\`bash
GET /api/model/info
\`\`\`

### 3. Health Check
\`\`\`bash
GET /health
\`\`\`

## Como Adicionar Seu Modelo Treinado

### Opção 1: Modelo Scikit-learn

Se você tem um modelo treinado com scikit-learn:

\`\`\`python
# Salvar seu modelo
import pickle

with open('gunshot_model.pkl', 'wb') as f:
    pickle.dump(seu_modelo, f)

# Criar arquivo de configuração
import json

config = {
    "name": "Modelo Jhon",
    "version": "1.0.0",
    "type": "random_forest",
    "description": "Modelo treinado com dataset de tiros",
    "trained_date": "2025-10-08",
    "accuracy": 0.92
}

with open('model_config.json', 'w') as f:
    json.dump(config, f)
\`\`\`

Coloque os arquivos na pasta `models/`:
\`\`\`bash
mkdir -p models
cp gunshot_model.pkl models/
cp model_config.json models/
\`\`\`

### Opção 2: Treinar Novo Modelo

Se você precisa treinar um novo modelo, crie um script:

\`\`\`python
# backend/train_model.py
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# Seus dados de treinamento
X = []  # Features extraídas de áudios
y = []  # Labels (0 = não é tiro, 1 = é tiro)

# Treinar modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Avaliar
accuracy = model.score(X_test, y_test)
print(f"Acurácia: {accuracy}")

# Salvar
with open('/app/models/gunshot_model.pkl', 'wb') as f:
    pickle.dump(model, f)
\`\`\`

Execute dentro do container:
\`\`\`bash
docker-compose exec backend python train_model.py
\`\`\`

## Modelo Atual

O sistema atualmente usa um **detector baseado em regras** que analisa:

1. **Energia do sinal** - Tiros têm picos de energia altos
2. **Frequência dominante** - Tiros geralmente entre 100-4000 Hz
3. **Zero Crossing Rate** - Transientes rápidos característicos
4. **Centroide espectral** - Distribuição de energia no espectro

Este modelo funciona bem para demonstração, mas um modelo de ML treinado terá melhor performance.

## Comandos Úteis

\`\`\`bash
# Ver logs do backend
docker-compose logs -f backend

# Ver logs do frontend
docker-compose logs -f frontend

# Reiniciar apenas o backend
docker-compose restart backend

# Recarregar modelo sem reiniciar
curl -X POST http://localhost:8000/api/model/reload

# Parar tudo
docker-compose down

# Limpar volumes e recomeçar
docker-compose down -v
docker-compose up --build
\`\`\`

## Próximos Passos

1. **Adicionar seu modelo treinado** na pasta `models/`
2. **Ajustar features** em `audio_processor.py` conforme seu modelo
3. **Testar com áudios reais** de tiros
4. **Ajustar thresholds** de confiança conforme necessário
5. **Adicionar mais endpoints** se necessário (batch processing, etc.)

## Troubleshooting

### Backend não inicia
\`\`\`bash
# Verificar logs
docker-compose logs backend

# Reconstruir imagem
docker-compose build --no-cache backend
\`\`\`

### Erro ao analisar áudio
- Verifique se o formato é suportado (.wav, .mp3, .m4a)
- Verifique os logs do backend
- Teste o endpoint diretamente: http://localhost:8000/docs

### Modelo não carrega
- Verifique se os arquivos estão em `models/`
- Verifique permissões dos arquivos
- O sistema usa modelo padrão se não encontrar o treinado
