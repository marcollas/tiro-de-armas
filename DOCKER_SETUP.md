# 🐳 Guia de Instalação Docker - Detector de Tiros

## Pré-requisitos

Apenas **Docker** e **Docker Compose** precisam estar instalados:

- [Instalar Docker](https://docs.docker.com/get-docker/)
- [Instalar Docker Compose](https://docs.docker.com/compose/install/)

**NÃO é necessário instalar:**
- ❌ Node.js
- ❌ npm
- ❌ Python
- ❌ Bibliotecas Python

Tudo roda dentro dos containers!

## 🚀 Como Rodar

### Opção 1: Comando Único (Recomendado)

\`\`\`bash
docker-compose up --build
\`\`\`

### Opção 2: Modo Detached (Background)

\`\`\`bash
docker-compose up -d --build
\`\`\`

### Opção 3: Usando o Script

\`\`\`bash
chmod +x scripts/docker-start.sh
./scripts/docker-start.sh
\`\`\`

## 📱 Acessar a Aplicação

Após iniciar os containers, acesse:

**http://localhost:3000**

## 🛠️ Comandos Úteis

### Ver logs em tempo real
\`\`\`bash
docker-compose logs -f
\`\`\`

### Ver logs apenas do frontend
\`\`\`bash
docker-compose logs -f frontend
\`\`\`

### Ver logs apenas do backend
\`\`\`bash
docker-compose logs -f python-backend
\`\`\`

### Parar os containers
\`\`\`bash
docker-compose down
\`\`\`

### Parar e remover volumes
\`\`\`bash
docker-compose down -v
\`\`\`

### Reconstruir do zero
\`\`\`bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up
\`\`\`

### Ver status dos containers
\`\`\`bash
docker-compose ps
\`\`\`

## 🔍 Verificar Saúde dos Serviços

\`\`\`bash
# Ver se os containers estão rodando
docker ps

# Verificar saúde do backend Python
docker exec gunshot-detector-backend python -c "import librosa; print('Backend OK')"

# Acessar shell do container frontend
docker exec -it gunshot-detector-frontend sh

# Acessar shell do container backend
docker exec -it gunshot-detector-backend sh
\`\`\`

## 📦 Estrutura dos Containers

### Frontend (Next.js)
- **Porta:** 3000
- **Imagem:** node:20-alpine
- **Build:** Standalone otimizado
- **Tamanho:** ~200MB

### Backend (Python)
- **Porta:** Interna (não exposta)
- **Imagem:** python:3.11-slim
- **Bibliotecas:** librosa, numpy, scipy, scikit-learn
- **Tamanho:** ~800MB

## 🔄 Atualizar a Aplicação

Após fazer mudanças no código:

\`\`\`bash
docker-compose down
docker-compose up --build
\`\`\`

## ⚠️ Solução de Problemas

### Porta 3000 já está em uso
\`\`\`bash
# Parar o processo usando a porta
lsof -ti:3000 | xargs kill -9

# Ou mudar a porta no docker-compose.yml
ports:
  - "3001:3000"  # Acesse em localhost:3001
\`\`\`

### Erro de permissão no volume
\`\`\`bash
docker-compose down -v
docker volume prune
docker-compose up --build
\`\`\`

### Container não inicia
\`\`\`bash
# Ver logs detalhados
docker-compose logs

# Reconstruir sem cache
docker-compose build --no-cache
\`\`\`

### Limpar tudo e começar do zero
\`\`\`bash
docker-compose down -v
docker system prune -a
docker-compose up --build
\`\`\`

## 💡 Dicas

- **Primeira execução:** Pode demorar 5-10 minutos para baixar e construir as imagens
- **Execuções seguintes:** Iniciam em segundos usando cache
- **Desenvolvimento:** Use `docker-compose.dev.yml` para hot reload
- **Produção:** Use `docker-compose.yml` padrão

## 🎯 Fluxo Completo

\`\`\`bash
# 1. Clone/baixe o projeto
cd gunshot-detector

# 2. Inicie os containers
docker-compose up --build

# 3. Acesse no navegador
# http://localhost:3000

# 4. Faça upload de um áudio e teste

# 5. Quando terminar
docker-compose down
\`\`\`

Pronto! Sua aplicação está rodando completamente em Docker sem precisar instalar nada localmente.
