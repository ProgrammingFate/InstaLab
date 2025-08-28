# Scripts do InstaLab

Esta pasta contém todos os scripts utilitários organizados por categoria.

## 📁 Estrutura das Pastas

### 🧪 test_data/
Scripts para criação de dados de teste:
- `create_test_users.py` - Cria usuários de teste (estudantes e empresas)

### 🛠️ management/
Scripts para gerenciamento do sistema:
- `manage_project_requests.py` - Sistema interativo para empresas gerenciarem candidaturas

### 📊 population/
Scripts para popular o banco de dados:
- `populate_categories.py` - Cria categorias padrão para vagas
- `populate_jobs.py` - Cria vagas de exemplo

## 🐳 Como usar com Docker

### Executar scripts de população:
```bash
# Popular categorias
sudo docker compose exec web python scripts/population/populate_categories.py

# Popular vagas de exemplo
sudo docker compose exec web python scripts/population/populate_jobs.py
```

### Executar scripts de teste:
```bash
# Criar usuários de teste
sudo docker compose exec web python scripts/test_data/create_test_users.py
```

### Executar scripts de gerenciamento:
```bash
# Sistema de gerenciamento de candidaturas para empresas
sudo docker compose exec web python scripts/management/manage_project_requests.py
```

## 📋 Comandos Django Management

Além dos scripts standalone, você também pode usar os comandos Django:

```bash
# Popular categorias
sudo docker compose exec web python manage.py populate_categories

# Gerenciar candidaturas
sudo docker compose exec web python manage.py manage_applications --help

# Setup completo de dados de teste
sudo docker compose exec web python manage.py setup_test_data
```

## 🚀 Setup Completo

Para configurar o ambiente completo de desenvolvimento:

```bash
# 1. Popular categorias
sudo docker compose exec web python scripts/population/populate_categories.py

# 2. Criar dados de teste
sudo docker compose exec web python scripts/test_data/create_test_users.py

# 3. Popular vagas de exemplo
sudo docker compose exec web python scripts/population/populate_jobs.py
```

Agora o sistema estará pronto com:
- ✅ 20 categorias de vagas
- ✅ Usuários de teste (empresa e estudante)
- ✅ Vagas de exemplo
- ✅ Sistema de gerenciamento funcional
