#!/bin/bash

echo "=================================================="
echo "  TREINAMENTO DO MODELO DE DETECÇÃO DE TIROS"
echo "=================================================="
echo ""

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Inicie o Docker primeiro."
    exit 1
fi

# Verificar se os dados existem
if [ ! -d "data/gunshots" ] || [ ! -d "data/non_gunshots" ]; then
    echo "⚠️  Diretórios de dados não encontrados!"
    echo ""
    echo "Criando estrutura de diretórios..."
    mkdir -p data/gunshots data/non_gunshots
    echo "✓ Diretórios criados"
    echo ""
    echo "📋 PRÓXIMOS PASSOS:"
    echo "  1. Adicione arquivos .wav de tiros em: data/gunshots/"
    echo "  2. Adicione arquivos .wav de não-tiros em: data/non_gunshots/"
    echo "  3. Execute este script novamente"
    echo ""
    echo "💡 Veja TRAINING_GUIDE.md para mais informações sobre datasets"
    exit 1
fi

# Contar arquivos
gunshots_count=$(find data/gunshots -name "*.wav" -o -name "*.mp3" | wc -l)
non_gunshots_count=$(find data/non_gunshots -name "*.wav" -o -name "*.mp3" | wc -l)

echo "📊 Dados encontrados:"
echo "  Tiros: $gunshots_count arquivos"
echo "  Não-tiros: $non_gunshots_count arquivos"
echo ""

if [ "$gunshots_count" -lt 10 ] || [ "$non_gunshots_count" -lt 10 ]; then
    echo "⚠️  Dados insuficientes para treinamento!"
    echo "   Recomendado: pelo menos 100 amostras de cada classe"
    echo ""
    read -p "Deseja continuar mesmo assim? (s/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi

echo "🚀 Iniciando treinamento..."
echo ""

# Verificar se o container está rodando
if ! docker ps | grep -q gunshot-detector-backend; then
    echo "⚠️  Container do backend não está rodando"
    echo "   Iniciando containers..."
    docker-compose up -d
    echo "   Aguardando backend ficar pronto..."
    sleep 10
fi

# Executar treinamento no container
echo "🤖 Executando script de treinamento..."
docker exec -it gunshot-detector-backend python ml/train_gunshot_detector.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "✓ TREINAMENTO CONCLUÍDO COM SUCESSO!"
    echo "=================================================="
    echo ""
    echo "📋 PRÓXIMOS PASSOS:"
    echo "  1. Teste o modelo: docker exec -it gunshot-detector-backend python ml/test_model.py <audio.wav>"
    echo "  2. Recarregue o backend: docker-compose restart backend"
    echo "  3. Acesse a aplicação: http://localhost:3000"
    echo ""
else
    echo ""
    echo "❌ Erro durante o treinamento"
    echo "   Verifique os logs acima para mais detalhes"
    exit 1
fi
