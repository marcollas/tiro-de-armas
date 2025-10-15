# Quick Demo: Gunshot Detector (Back + Front)

Este guia ajuda você a apresentar rapidamente o projeto: subir o backend (FastAPI) e o frontend (Next.js), treinar o modelo (opcional) e fazer um teste de análise de áudio.

## Requisitos

- Docker e Docker Compose (recomendado) OU Python 3.10+ e Node.js 18+
- Arquivos de áudio `.wav` para teste

## 1) Subir com Docker (back + front)

- Subir os serviços:

```bash
# na raiz do repositório
docker-compose up --build -d
# ver logs
docker-compose logs -f
```

- Backend: http://localhost:8000
  - Health: http://localhost:8000/health
  - Docs (Swagger): http://localhost:8000/docs
- Frontend: http://localhost:3000

## 2) Testar o backend (sem treinar)

Mesmo sem modelo ML treinado, o backend funciona com um detector rule-based.

```bash
# Health
curl -s http://localhost:8000/health | jq .

# Info do modelo
curl -s http://localhost:8000/api/model/info | jq .

# Analisar um áudio (substitua o caminho para um .wav)
curl -s -F "file=@augmented/gunshots/148837-6-0-0.wav" http://localhost:8000/api/analyze | jq .
```

## 3) Treinar o modelo (opcional, melhora resultados)

Coloque seus dados:

- `data/gunshots/` – áudios de tiros (.wav)
- `data/non_gunshots/` – áudios de não-tiros (.wav)

Treinar:

```bash
# dentro do container backend
docker exec -it gunshot-detector-backend python ml/train_gunshot_detector.py

# ou localmente (requer Python e dependências do backend)
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python ml/train_gunshot_detector.py
```

Isso salva:

- `models/gunshot_detector.pkl`
- `models/model_metadata.json`
- `models/scaler.joblib`

Reinicie o backend para carregar o novo modelo:

```bash
docker-compose restart backend
# ou, se rodando localmente com uvicorn, pare e inicie de novo
```

## 4) Subir localmente (sem Docker)

Backend:

```bash
python -m venv .venv_local
source .venv_local/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload
# Health: http://localhost:8001/health
```

Frontend:

```bash
# Node 18+, PNPM ou NPM
pnpm install  # ou npm install
pnpm dev      # ou npm run dev
# http://localhost:3000
```

## 5) Dicas para a apresentação

- Abra o Swagger em `/docs` e faça um upload de áudio no `/api/analyze`.
- Mostre o `GET /api/model/info` para provar que o modelo foi carregado.
- Se o modelo ML estiver ausente, explique que o sistema usa fallback rule-based.

## 6) Observações

- Este repositório ignora datasets, venvs e arquivos grandes de modelo.
- Veja `TRAINING_GUIDE.md` para detalhes adicionais de datasets e treinamento.
