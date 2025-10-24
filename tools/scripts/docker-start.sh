#!/bin/bash

echo "🐳 Iniciando Detector de Tiros com Docker..."
echo ""

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale o Docker primeiro."
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
    exit 1
fi

# Criar diretório temp se não existir
mkdir -p temp

echo "✅ Pré-requisitos verificados"
echo ""
echo "🔨 Construindo containers..."
docker-compose build

echo ""
echo "🚀 Iniciando aplicação..."
docker-compose up -d

echo ""
echo "⏳ Aguardando containers iniciarem..."
sleep 5

echo ""
echo "✅ Aplicação iniciada com sucesso!"
echo ""
echo "📱 Acesse: http://localhost:3000"
echo ""
echo "📊 Ver logs: docker-compose logs -f"
echo "🛑 Parar: docker-compose down"
echo ""
