# Detector de Tiros com IA

Uma aplicação web moderna para detecção de tiros em arquivos de áudio usando inteligência artificial e processamento de sinais digitais.

## 🚀 Características

- **Interface moderna**: Design limpo inspirado em estúdios de IA
- **Análise em tempo real**: Processamento de áudio com feedback visual
- **Backend Python**: Algoritmos avançados de detecção usando librosa e scipy
- **Histórico de análises**: Acompanhe todas as análises anteriores
- **Reprodução de áudio**: Player integrado para revisar os arquivos analisados

## 📋 Pré-requisitos

### Frontend (Next.js)
- Node.js 18+ 
- npm ou yarn

### Backend (Python)
- Python 3.8+
- pip (gerenciador de pacotes Python)

## 🛠️ Instalação

### 1. Clone e configure o frontend

\`\`\`bash
# Baixe o projeto do v0
# Clique nos três pontos → "Download ZIP"

# Instale as dependências
npm install

# Inicie o servidor de desenvolvimento
npm run dev
\`\`\`

### 2. Configure o backend Python

\`\`\`bash
# Crie um ambiente virtual (recomendado)
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale as dependências Python
pip install librosa numpy scipy scikit-learn matplotlib soundfile

# Crie a pasta temp na raiz do projeto
mkdir temp
\`\`\`

### 3. Teste a integração

\`\`\`bash
# Teste o detector Python
python scripts/audio_analyzer.py caminho/para/seu/audio.wav

# Teste com áudio sintético
python scripts/test_detector.py
\`\`\`

## 🎯 Como usar

1. **Acesse** `http://localhost:3000`
2. **Faça upload** de um arquivo de áudio (.wav, .mp3, .m4a)
3. **Clique** em "Iniciar Análise"
4. **Aguarde** o processamento (alguns segundos)
5. **Visualize** os resultados com confiança e detalhes técnicos

## 🔧 Solução de problemas

### Erro: "Python não encontrado"
- Certifique-se que o Python está instalado e no PATH do sistema
- Teste executando `python --version` no terminal

### Erro: "Módulo não encontrado"
- Instale as dependências: `pip install librosa numpy scipy scikit-learn`
- Verifique se o ambiente virtual está ativado

### Erro: "Pasta temp não encontrada"
- Crie a pasta manualmente: `mkdir temp` na raiz do projeto

## 📁 Estrutura do projeto

\`\`\`
├── app/
│   ├── api/analyze-audio/route.ts    # API endpoint para análise
│   ├── page.tsx                      # Página principal
│   └── layout.tsx                    # Layout da aplicação
├── components/
│   ├── header.tsx                    # Cabeçalho
│   ├── sidebar.tsx                   # Barra lateral
│   ├── audio-upload.tsx              # Upload de áudio
│   ├── audio-analysis.tsx            # Interface de análise
│   └── analysis-results.tsx          # Resultados
├── scripts/
│   ├── audio_analyzer.py             # Detector principal
│   ├── test_detector.py              # Testes
│   └── batch_analyzer.py             # Análise em lote
└── temp/                             # Arquivos temporários
\`\`\`

## 🧠 Como funciona

O sistema usa técnicas avançadas de processamento de sinais digitais:

- **Análise temporal**: Duração, energia RMS, taxa de cruzamento por zero
- **Análise espectral**: Centroide, rolloff, largura de banda
- **MFCC**: Coeficientes cepstrais mel-frequency
- **Detecção de onset**: Identificação de início súbito
- **Classificação**: Algoritmo de pontuação baseado em características típicas de tiros

## 📊 Precisão

O detector foi otimizado para identificar:
- ✅ Tiros de armas de fogo
- ✅ Explosões pequenas
- ✅ Estouros súbitos

Pode confundir com:
- ⚠️ Fogos de artifício
- ⚠️ Batidas de porta muito fortes
- ⚠️ Balões estourando

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.
