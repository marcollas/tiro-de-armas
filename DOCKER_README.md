# Guia Docker - Detector de Tiros

## Pré-requisitos

- Docker instalado (versão 20.10+)
- Docker Compose instalado (versão 2.0+)

## Comandos Rápidos

### Produção

\`\`\`bash
# Construir e iniciar os containers
docker-compose up --build

# Iniciar em background
docker-compose up -d

# Parar os containers
docker-compose down

# Ver logs
docker-compose logs -f

# Ver logs apenas do frontend
docker-compose logs -f frontend

# Ver logs apenas do backend
docker-compose logs -f python-backend
\`\`\`

### Desenvolvimento

\`\`\`bash
# Iniciar em modo desenvolvimento
docker-compose -f docker-compose.dev.yml up --build

# Parar
docker-compose -f docker-compose.dev.yml down
\`\`\`

## Estrutura dos Containers

### Frontend (Next.js)
- **Porta:** 3000
- **Container:** gunshot-detector-frontend
- **Volumes:** 
  - `./temp` - Arquivos de áudio temporários
  - `./scripts` - Scripts Python

### Backend (Python)
- **Container:** gunshot-detector-backend
- **Volumes:**
  - `./scripts` - Scripts Python
  - `./temp` - Arquivos de áudio compartilhados

## Acessando a Aplicação

Após iniciar os containers, acesse:
- **Frontend:** http://localhost:3000

## Resolução de Problemas

### Container não inicia
\`\`\`bash
# Ver logs detalhados
docker-compose logs

# Reconstruir sem cache
docker-compose build --no-cache
docker-compose up
\`\`\`

### Limpar tudo e recomeçar
\`\`\`bash
# Parar e remover containers, volumes e imagens
docker-compose down -v
docker system prune -a

# Reconstruir
docker-compose up --build
\`\`\`

### Verificar status dos containers
\`\`\`bash
docker-compose ps
\`\`\`

### Executar comandos dentro dos containers
\`\`\`bash
# Acessar shell do frontend
docker exec -it gunshot-detector-frontend sh

# Acessar shell do backend Python
docker exec -it gunshot-detector-backend bash

# Testar script Python manualmente
docker exec -it gunshot-detector-backend python scripts/setup_check.py
\`\`\`

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto se precisar customizar:

\`\`\`env
# Porta do frontend
FRONTEND_PORT=3000

# Ambiente
NODE_ENV=production
\`\`\`

## Volumes Persistentes

Os arquivos de áudio temporários são compartilhados entre os containers através do volume `./temp`.

## Rede

Os containers se comunicam através da rede `app-network` criada pelo Docker Compose.

## Atualizações

Para atualizar a aplicação:

\`\`\`bash
# Parar containers
docker-compose down

# Atualizar código (git pull, etc)

# Reconstruir e iniciar
docker-compose up --build
