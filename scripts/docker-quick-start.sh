#!/bin/bash

echo "🐳 Iniciando Detector de Tiros com Docker..."
echo ""
echo "Verificando Docker..."

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado!"
    echo "Instale em: https://docs.docker.com/get-docker/"
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado!"
    echo "Instale em: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker encontrado"
echo ""

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker-compose down 2>/dev/null

echo ""
echo "🔨 Construindo e iniciando containers..."
echo "⏳ Isso pode demorar alguns minutos na primeira vez..."
echo ""

# Construir e iniciar
docker-compose up --build

# Se o usuário pressionar Ctrl+C
trap 'echo ""; echo "🛑 Parando containers..."; docker-compose down; exit 0' INT

echo ""
echo "✅ Aplicação rodando em http://localhost:3000"
echo "📋 Pressione Ctrl+C para parar"
