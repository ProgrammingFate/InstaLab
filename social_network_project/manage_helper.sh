#!/bin/bash

# InstaLab - Script de Comandos Úteis
# Este script fornece comandos úteis para desenvolvimento

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== InstaLab - Comandos Úteis ===${NC}\n"

# Função para executar comandos
execute_command() {
    echo -e "${YELLOW}Executando: $1${NC}"
    eval $1
    echo ""
}

# Menu
echo "Escolha uma opção:"
echo "1) Criar migrações"
echo "2) Aplicar migrações"
echo "3) Criar superusuário"
echo "4) Executar servidor de desenvolvimento"
echo "5) Executar testes"
echo "6) Executar testes com coverage"
echo "7) Criar dados de teste"
echo "8) Limpar banco de dados"
echo "9) Instalar/Atualizar dependências"
echo "10) Coletar arquivos estáticos"
echo "11) Criar arquivo de logs"
echo "12) Verificar erros de código (flake8)"
echo "13) Executar shell Django"
echo "14) Backup do banco de dados"
echo "15) Gerar SECRET_KEY nova"
echo "0) Sair"

read -p "Digite o número da opção: " option

case $option in
    1)
        execute_command "python manage.py makemigrations"
        ;;
    2)
        execute_command "python manage.py migrate"
        ;;
    3)
        execute_command "python manage.py createsuperuser"
        ;;
    4)
        execute_command "python manage.py runserver 8001"
        ;;
    5)
        execute_command "python manage.py test"
        ;;
    6)
        echo -e "${YELLOW}Instalando coverage se necessário...${NC}"
        pip install coverage > /dev/null 2>&1
        execute_command "coverage run --source='.' manage.py test"
        execute_command "coverage report"
        execute_command "coverage html"
        echo -e "${GREEN}Relatório HTML gerado em htmlcov/index.html${NC}"
        ;;
    7)
        echo -e "${YELLOW}Criando dados de teste...${NC}"
        execute_command "python scripts/test_data/create_test_users.py"
        execute_command "python scripts/population/populate_categories.py"
        execute_command "python scripts/population/populate_jobs.py"
        ;;
    8)
        read -p "Tem certeza que deseja limpar o banco de dados? (s/N): " confirm
        if [ "$confirm" == "s" ] || [ "$confirm" == "S" ]; then
            execute_command "rm -f db.sqlite3"
            execute_command "python manage.py migrate"
            echo -e "${GREEN}Banco de dados limpo!${NC}"
        fi
        ;;
    9)
        execute_command "pip install -r requirements.txt"
        ;;
    10)
        execute_command "python manage.py collectstatic --noinput"
        ;;
    11)
        execute_command "mkdir -p logs"
        execute_command "touch logs/django.log"
        echo -e "${GREEN}Diretório de logs criado!${NC}"
        ;;
    12)
        echo -e "${YELLOW}Instalando flake8 se necessário...${NC}"
        pip install flake8 > /dev/null 2>&1
        execute_command "flake8 apps/ config/ --max-line-length=120 --exclude=migrations"
        ;;
    13)
        execute_command "python manage.py shell"
        ;;
    14)
        timestamp=$(date +%Y%m%d_%H%M%S)
        backup_file="db_backup_${timestamp}.sqlite3"
        execute_command "cp db.sqlite3 ${backup_file}"
        echo -e "${GREEN}Backup criado: ${backup_file}${NC}"
        ;;
    15)
        echo -e "${YELLOW}Gerando nova SECRET_KEY...${NC}"
        python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
        ;;
    0)
        echo -e "${GREEN}Saindo...${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Opção inválida!${NC}"
        exit 1
        ;;
esac
