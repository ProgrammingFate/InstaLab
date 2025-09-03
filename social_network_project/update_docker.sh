#!/bin/bash

echo "🔄 Atualizando projeto Docker com novas alterações..."

# Opção para rebuild completo
if [ "$1" = "--rebuild" ]; then
    echo "🔨 Fazendo rebuild completo dos containers..."
    sudo docker compose down
    sudo docker compose build --no-cache
    sudo docker compose up -d
    echo "✅ Rebuild completo concluído!"
else
    # Coletar arquivos estáticos atualizados
    echo "📦 Coletando arquivos estáticos..."
    sudo docker compose exec web python manage.py collectstatic --noinput

    # Reiniciar o container web para aplicar mudanças
    echo "🔄 Reiniciando container web..."
    sudo docker compose restart web
fi

# Verificar status dos containers
echo "✅ Verificando status dos containers..."
sudo docker compose ps

echo "🎉 Atualização concluída! Acesse: http://localhost:8000"
echo ""
echo "💡 Dicas:"
echo "   - Para mudanças simples (CSS/HTML): ./update_docker.sh"
echo "   - Para mudanças no Dockerfile/requirements: ./update_docker.sh --rebuild"
