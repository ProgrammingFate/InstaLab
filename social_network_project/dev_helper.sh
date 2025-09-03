#!/bin/bash

# Script para comparar ambiente virtual vs Docker
# Útil para debug quando há diferenças entre os ambientes

echo "🔍 Comparando Ambiente Virtual vs Docker..."
echo ""

echo "📋 AMBIENTE VIRTUAL (venv):"
echo "   URL: http://localhost:8001 (quando rodando)"
echo "   Comando: venv/bin/python manage.py runserver 0.0.0.0:8001"
echo ""

echo "🐳 DOCKER COMPOSE:"
echo "   URL: http://localhost:8000"
echo "   Status atual:"
sudo docker compose ps
echo ""

echo "📁 Arquivos importantes sincronizados:"
echo "   ✅ static/css/main.css"
echo "   ✅ apps/core/templates/core/base.html"
echo "   ✅ apps/accounts/templates/accounts/login.html"
echo ""

echo "🛠️ Comandos úteis:"
echo "   Atualizar Docker:     ./update_docker.sh"
echo "   Rebuild completo:     ./update_docker.sh --rebuild"
echo "   Parar Docker:         sudo docker compose down"
echo "   Iniciar Docker:       sudo docker compose up -d"
echo "   Ver logs:             sudo docker compose logs web"
echo ""

echo "🔧 Para desenvolvimento:"
echo "   1. Faça alterações nos arquivos"
echo "   2. Teste no venv: venv/bin/python manage.py runserver 0.0.0.0:8001"
echo "   3. Quando satisfeito, atualize Docker: ./update_docker.sh"
