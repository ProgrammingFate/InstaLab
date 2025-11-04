#!/bin/bash

# Script para reconstruir e iniciar o Docker com as novas dependências

echo "🐳 Reconstruindo InstaLab Docker..."
echo ""

cd /home/lucas-dev/Desktop/projects/instalab/InstaLab/social_network_project

echo "1️⃣ Parando containers existentes..."
docker compose down

echo ""
echo "2️⃣ Reconstruindo imagem (isso pode demorar alguns minutos)..."
docker compose build

echo ""
echo "3️⃣ Iniciando containers..."
docker compose up -d

echo ""
echo "4️⃣ Aguardando inicialização..."
sleep 10

echo ""
echo "5️⃣ Verificando logs..."
docker compose logs web | tail -20

echo ""
echo "✅ Docker reconstruído!"
echo ""
echo "Para ver logs: docker compose logs -f web"
echo "Para acessar: http://localhost:8000"
echo "Para parar: docker compose down"
