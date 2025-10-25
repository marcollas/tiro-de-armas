# Detector de Tiros com IA

Uma aplicação web moderna para detecção de tiros em arquivos de áudio usando inteligência artificial (EfficientNet) e processamento de sinais digitais.

## 🚀 Características

- **Interface moderna**: Design limpo e responsivo com Next.js 15
- **Modelo EfficientNet**: Rede neural convolucional otimizada para classificação de áudio
- **Análise em tempo real**: Processamento de áudio com feedback visual
- **Backend FastAPI**: API robusta e escalável em Python
- **Histórico de análises**: Acompanhe todas as análises anteriores
- **Reprodução de áudio**: Player integrado para revisar os arquivos analisados
- **Docker**: Setup completo com containerização

## 📋 Pré-requisitos

### Opção 1: Docker (Recomendado)

- Docker 20.10+
- Docker Compose 2.0+

### Opção 2: Instalação Manual

- Node.js 20+
- Python 3.11+
- npm ou pnpm

## 🐳 Instalação com Docker (Recomendado)

### Início Rápido

```bash
# Clone o repositório
git clone <seu-repositorio>
cd gunshot-detector

# Inicie com Docker Compose
docker-compose up --build

# Ou use o script auxiliar
chmod +x tools/scripts/docker-quick-start.sh
./tools/scripts/docker-quick-start.sh
```

Acesse: **http://localhost:3000**

### Comandos Docker Úteis

```bash
# Ver logs em tempo real
docker-compose logs -f

# Ver logs apenas do backend
docker-compose logs -f backend

# Ver logs apenas do frontend
docker-compose logs -f frontend

# Parar a aplicação
docker-compose down

# Reconstruir do zero
docker-compose down && docker-compose up --build
```

## 🛠️ Instalação Manual

### 1. Frontend (Next.js)

```bash
# Instalar dependências
npm install

# Modo desenvolvimento
npm run dev

# Build para produção
npm run build
npm start
```

### 2. Backend (Python/FastAPI)

```bash
# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Instalar dependências
cd backend
pip install -r requirements.txt

# Iniciar servidor FastAPI
python main.py
```

O backend estará disponível em: **http://localhost:8000**
Documentação da API: **http://localhost:8000/docs**

## 🎯 Como Usar

1. Acesse **http://localhost:3000**
2. Faça upload de um arquivo de áudio (.wav, .mp3, .m4a, .flac, .ogg)
3. Clique em **"Analisar Áudio"**
4. Aguarde o processamento (alguns segundos)
5. Visualize os resultados detalhados:
   - Tiro detectado ou não
   - Confiança da predição
   - Características do áudio
   - Método de detecção usado

## 📁 Estrutura do Projeto

```
gunshot-detector/
├── app/                          # Frontend Next.js
│   ├── api/analyze-audio/       # API route para análise
│   ├── page.tsx                 # Página principal
│   ├── layout.tsx               # Layout da aplicação
│   └── globals.css              # Estilos globais
├── backend/                      # Backend FastAPI
│   ├── main.py                  # Servidor FastAPI
│   ├── model_loader.py          # Carregamento do modelo
│   ├── audio_processor.py       # Processamento de áudio
│   ├── generate_audio_graphs.py # Geração de gráficos
│   └── requirements.txt         # Dependências Python
├── components/                   # Componentes React
│   ├── header.tsx
│   ├── sidebar.tsx
│   ├── audio-upload.tsx
│   ├── audio-analysis.tsx
│   ├── analysis-results.tsx
│   └── ui/                      # Componentes shadcn/ui
├── tools/                        # Ferramentas de desenvolvimento
│   ├── ml/                      # Scripts de treinamento ML
│   │   ├── train_gunshot_detector.py
│   │   ├── test_model.py
│   │   ├── download_dataset.py
│   │   └── augment_data.py
│   └── scripts/                 # Scripts auxiliares
│       ├── audio_analyzer.py
│       ├── batch_analyzer.py
│       ├── setup_check.py
│       └── docker-*.sh
├── IA_EfficientNet_test/        # Modelo treinado EfficientNet
│   ├── config.json
│   ├── metadata.json
│   └── model.weights.h5
├── docker-compose.yml           # Orquestração Docker
├── Dockerfile                   # Build frontend
├── Dockerfile.backend           # Build backend
└── package.json                 # Dependências Node.js
```

## 🧠 Como Funciona

### Modelo EfficientNet

O sistema usa um modelo **EfficientNet** treinado especificamente para detecção de tiros:

1. **Pré-processamento**: Áudio convertido em espectrogramas mel
2. **Extração de Features**: MFCCs, energia, centroide espectral, rolloff
3. **Classificação**: Rede neural identifica padrões característicos de tiros
4. **Fallback**: Sistema rule-based como backup se o modelo não estiver disponível

### Pipeline de Análise

```
Áudio Input
    ↓
Pré-processamento (librosa)
    ↓
Extração de Features
    ↓
Modelo EfficientNet
    ↓
Predição (Tiro/Não-Tiro + Confiança)
    ↓
Resultado + Visualizações
```

## 🎓 Treinamento do Modelo

### Preparar Dados

```bash
# Criar estrutura de diretórios
mkdir -p data/gunshots data/non_gunshots

# Adicionar seus áudios:
# - data/gunshots/     → arquivos .wav de tiros
# - data/non_gunshots/ → arquivos .wav de não-tiros
```

### Fontes de Dados Recomendadas

**UrbanSound8K**

- URL: https://urbansounddataset.weebly.com/urbansound8k.html
- 8732 sons urbanos incluindo tiros
- Formato: WAV, 4 segundos cada

**Freesound.org**

- URL: https://freesound.org/search/?q=gunshot
- Milhares de sons de tiros
- Licença Creative Commons

**AudioSet (Google)**

- URL: https://research.google.com/audioset/
- Categoria: "Gunshot, gunfire"

### Executar Treinamento

```bash
# Opção 1: Com Docker
chmod +x tools/scripts/train-model.sh
./tools/scripts/train-model.sh

# Opção 2: Localmente
python tools/ml/train_gunshot_detector.py
```

### Testar Modelo

```bash
# Testar um áudio específico
python tools/ml/test_model.py audio.wav

# Testar múltiplos áudios
python tools/ml/test_model.py --batch diretorio/
```

### Data Augmentation

```bash
# Aumentar dataset com variações
python tools/ml/augment_data.py data/gunshots/ augmented/gunshots/
python tools/ml/augment_data.py data/non_gunshots/ augmented/non_gunshots/
```

## 🔧 Solução de Problemas

### Docker

**Erro: "Cannot connect to Docker daemon"**

```bash
# Verificar se Docker está rodando
sudo systemctl start docker  # Linux
# ou inicie o Docker Desktop
```

**Erro: "Port 3000 already in use"**

```bash
# Parar containers conflitantes
docker-compose down
# ou mudar porta no docker-compose.yml
```

### Backend

**Erro: "Model not loading"**

- Verifique se `IA_EfficientNet_test/` existe
- Confirme que `model.weights.h5` está presente
- Verifique logs: `docker-compose logs backend`

**Erro: "TensorFlow not found"**

```bash
# Reinstalar dependências
pip install -r backend/requirements.txt
```

### Frontend

**Erro: "Cannot reach backend"**

- Verifique se backend está rodando: http://localhost:8000/health
- Confirme variáveis de ambiente em `docker-compose.yml`

## 🧪 Testes

### Testar Backend Isoladamente

```bash
# Health check
curl http://localhost:8000/health

# Info do modelo
curl http://localhost:8000/api/model/info

# Analisar áudio (substitua o caminho)
curl -F "file=@audio.wav" http://localhost:8000/api/analyze
```

### Análise em Lote

```bash
# Analisar diretório completo
python tools/scripts/batch_analyzer.py diretorio/ resultados.json
```

## 📊 Precisão e Limitações

### O que detecta bem:

- ✅ Tiros de armas de fogo (pistolas, rifles)
- ✅ Disparos únicos e rajadas
- ✅ Diferentes distâncias de gravação
- ✅ Ambientes internos e externos

### Pode confundir com:

- ⚠️ Fogos de artifício (padrão acústico similar)
- ⚠️ Batidas de porta muito fortes
- ⚠️ Balões estourando
- ⚠️ Trovões

### Recomendações:

- Use dados de treinamento diversos
- Inclua sons "difíceis" nos não-tiros
- Ajuste threshold de confiança conforme necessidade
- Considere contexto adicional em aplicações críticas

## 🚀 Deploy em Produção

### Docker Compose

```bash
# Build para produção
docker-compose -f docker-compose.yml up --build -d
```

### Variáveis de Ambiente

```env
# Backend
PYTHONUNBUFFERED=1

# Frontend
NODE_ENV=production
BACKEND_API_URL=http://backend:8000
```

## 🔐 Segurança

- ⚠️ Não exponha a API publicamente sem autenticação
- 🔒 Use HTTPS em produção
- 🛡️ Implemente rate limiting
- 📝 Valide e sanitize todos os uploads
- 🚫 Limite tamanho de arquivos

## 🛠️ Tecnologias Utilizadas

### Frontend

- **Next.js 15** - Framework React
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - Componentes UI
- **Lucide React** - Ícones

### Backend

- **FastAPI** - Framework web Python
- **TensorFlow 2.15** - Deep Learning
- **Keras 2.15** - API de alto nível
- **Librosa 0.10** - Processamento de áudio
- **NumPy/SciPy** - Computação científica

### DevOps

- **Docker** - Containerização
- **Docker Compose** - Orquestração

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 VSCode Tasks

O projeto inclui tasks configuradas no VSCode:

- `Ctrl+Shift+B` → **Docker: Start Application**
- **Docker: Stop Application**
- **Docker: Rebuild**
- **Docker: View Logs**

## 📄 Licença

Este projeto está sob a licença MIT.

## 👥 Autores

- **Marcos** - Desenvolvimento inicial

## 📞 Suporte

Para questões e suporte:

- Abra uma issue no GitHub
- Consulte a documentação da API em `/docs` quando rodando

---

**Nota**: Este é um projeto educacional/acadêmico. Para aplicações críticas de segurança, considere adicionar camadas extras de validação e integração com sistemas especializados.
