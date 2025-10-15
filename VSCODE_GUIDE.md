# Guia VSCode - Detector de Tiros AI

## Configuração Inicial

### 1. Extensões Recomendadas
Instale as extensões sugeridas quando o VSCode perguntar, ou instale manualmente:
- **Docker** - Gerenciar containers visualmente
- **ESLint** - Linting para TypeScript/JavaScript
- **Prettier** - Formatação de código
- **Python** - Suporte para Python
- **Tailwind CSS IntelliSense** - Autocomplete para Tailwind

### 2. Rodar a Aplicação

#### Opção A: Usando Tasks (Recomendado)
1. Pressione `Ctrl+Shift+B` (ou `Cmd+Shift+B` no Mac)
2. Selecione "Docker: Start Application"
3. Aguarde o build completar

#### Opção B: Terminal Integrado
1. Pressione `` Ctrl+` `` para abrir o terminal
2. Execute: `docker-compose up --build`

### 3. Acessar a Aplicação
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Documentação API: http://localhost:8000/docs

## Testando a Aplicação

### 1. Teste Básico
1. Acesse http://localhost:3000
2. Faça upload de um arquivo de áudio (.wav, .mp3, .m4a)
3. Clique em "Analisar Áudio"
4. Verifique os resultados

### 2. Teste da API Backend
Abra http://localhost:8000/docs para ver a documentação interativa do FastAPI.

### 3. Ver Logs em Tempo Real
- Use a task "Docker: View Logs"
- Ou no terminal: `docker-compose logs -f`

## Comandos Úteis no Terminal

\`\`\`bash
# Iniciar aplicação
docker-compose up --build

# Parar aplicação
docker-compose down

# Ver logs
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f frontend
docker-compose logs -f backend

# Reconstruir tudo do zero
docker-compose down -v
docker-compose up --build

# Entrar no container (debug)
docker-compose exec frontend sh
docker-compose exec backend bash
\`\`\`

## Estrutura do Projeto

\`\`\`
gunshot-detector/
├── app/                    # Frontend Next.js
│   ├── api/               # API Routes
│   └── page.tsx           # Página principal
├── backend/               # Backend FastAPI
│   ├── main.py           # API principal
│   ├── model_loader.py   # Carregamento do modelo
│   └── audio_processor.py # Processamento de áudio
├── components/            # Componentes React
├── docker-compose.yml     # Orquestração Docker
└── .vscode/              # Configurações VSCode
\`\`\`

## Debugging

### Frontend (Next.js)
1. Adicione `console.log("[v0] ...")` no código
2. Abra DevTools do navegador (F12)
3. Veja os logs no Console

### Backend (FastAPI)
1. Veja os logs no terminal: `docker-compose logs -f backend`
2. Use a documentação interativa: http://localhost:8000/docs
3. Teste endpoints diretamente na interface Swagger

## Dicas de Produtividade

### Atalhos Úteis
- `Ctrl+Shift+B` - Executar task de build
- `` Ctrl+` `` - Abrir/fechar terminal
- `Ctrl+P` - Buscar arquivos rapidamente
- `Ctrl+Shift+F` - Buscar em todos os arquivos
- `F12` - Ir para definição

### Extensão Docker
1. Clique no ícone Docker na barra lateral
2. Veja containers, imagens e volumes
3. Clique com botão direito para ações rápidas
4. Veja logs diretamente na interface

### Live Reload
- Frontend: Mudanças em arquivos `.tsx` recarregam automaticamente
- Backend: Mudanças em arquivos `.py` reiniciam o servidor automaticamente

## Troubleshooting

### Porta já em uso
\`\`\`bash
# Parar todos os containers
docker-compose down

# Verificar portas em uso
# Linux/Mac:
lsof -i :3000
lsof -i :8000

# Windows:
netstat -ano | findstr :3000
netstat -ano | findstr :8000
\`\`\`

### Rebuild completo
\`\`\`bash
docker-compose down -v
docker system prune -a
docker-compose up --build
\`\`\`

### Problemas com cache
\`\`\`bash
docker-compose build --no-cache
docker-compose up
