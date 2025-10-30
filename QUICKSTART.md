# 🚀 Guia Rápido - InstaLab

## 📦 Instalação e Configuração

### 1. Clonar o Repositório
```bash
git clone https://github.com/ProgrammingFate/InstaLab.git
cd InstaLab/social_network_project
```

### 2. Criar Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
```bash
cp .env.example .env
nano .env  # Edite as variáveis necessárias
```

### 5. Criar Diretório de Logs
```bash
mkdir logs
```

### 6. Executar Migrações
```bash
python manage.py migrate
```

### 7. Criar Superusuário
```bash
python manage.py createsuperuser
```

### 8. (Opcional) Criar Dados de Teste
```bash
python scripts/test_data/create_test_users.py
python scripts/population/populate_categories.py
python scripts/population/populate_jobs.py
```

### 9. Executar Servidor
```bash
python manage.py runserver 8001
```

Acesse: http://localhost:8001

---

## 🔑 Variáveis de Ambiente Importantes

Edite o arquivo `.env`:

```env
# Desenvolvimento
DEBUG=True
SECRET_KEY=sua-secret-key-aqui

# Produção
DEBUG=False
SECRET_KEY=use-uma-key-forte-e-aleatoria
ALLOWED_HOSTS=seudominio.com,www.seudominio.com

# Banco de Dados (Produção)
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=instalab_db
DATABASE_USER=seu_usuario
DATABASE_PASSWORD=sua_senha
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Cache (Produção)
CACHE_ENABLED=True
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

## 🧪 Executar Testes

### Todos os testes
```bash
python manage.py test
```

### App específico
```bash
python manage.py test apps.core
python manage.py test apps.accounts
```

### Com coverage
```bash
coverage run --source='.' manage.py test
coverage report
coverage html  # Gera relatório em htmlcov/
```

---

## 🔌 Usar a API

### 1. Obter Token JWT
```bash
curl -X POST http://localhost:8001/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "seu_usuario",
    "password": "sua_senha"
  }'
```

Resposta:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 2. Usar Token nas Requisições
```bash
curl http://localhost:8001/api/v1/posts/ \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN"
```

### 3. Renovar Token
```bash
curl -X POST http://localhost:8001/api/v1/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "SEU_REFRESH_TOKEN"
  }'
```

### 4. Ver Documentação Interativa
Acesse: http://localhost:8001/api/docs/

---

## 📡 Endpoints da API

### Autenticação
- `POST /api/v1/auth/token/` - Obter token
- `POST /api/v1/auth/token/refresh/` - Renovar token

### Usuários
- `GET /api/v1/users/` - Listar usuários
- `GET /api/v1/users/{id}/` - Detalhes do usuário
- `GET /api/v1/users/me/` - Perfil atual

### Posts
- `GET /api/v1/posts/` - Listar posts
- `POST /api/v1/posts/` - Criar post
- `GET /api/v1/posts/{id}/` - Detalhes
- `POST /api/v1/posts/{id}/like/` - Like/Unlike
- `POST /api/v1/posts/{id}/comment/` - Comentar

### Vagas
- `GET /api/v1/jobs/` - Listar vagas
- `POST /api/v1/jobs/` - Criar vaga (empresa)
- `GET /api/v1/jobs/{id}/` - Detalhes
- `POST /api/v1/jobs/{id}/apply/` - Candidatar-se
- `GET /api/v1/jobs/{id}/applications/` - Ver candidaturas

### Candidaturas
- `GET /api/v1/applications/` - Minhas candidaturas
- `PATCH /api/v1/applications/{id}/update_status/` - Atualizar status

---

## 🐳 Docker

### Construir e Executar
```bash
docker-compose up --build
```

### Executar Comandos no Container
```bash
docker-compose run --rm web python manage.py migrate
docker-compose run --rm web python manage.py createsuperuser
docker-compose run --rm web python manage.py test
```

### Parar Containers
```bash
docker-compose down
```

---

## 🛠️ Comandos Úteis

### Criar Migrações
```bash
python manage.py makemigrations
```

### Aplicar Migrações
```bash
python manage.py migrate
```

### Criar Superusuário
```bash
python manage.py createsuperuser
```

### Shell Django
```bash
python manage.py shell
```

### Coletar Arquivos Estáticos
```bash
python manage.py collectstatic
```

### Gerar SECRET_KEY Nova
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Verificar Problemas
```bash
python manage.py check
```

### Criar Backup do Banco
```bash
cp db.sqlite3 db_backup_$(date +%Y%m%d).sqlite3
```

### Script Helper (Linux/Mac)
```bash
chmod +x manage_helper.sh
./manage_helper.sh
```

---

## 📊 Monitoramento e Logs

### Ver Logs em Tempo Real
```bash
tail -f logs/django.log
```

### Verificar Tamanho dos Logs
```bash
du -h logs/
```

### Limpar Logs Antigos
```bash
find logs/ -name "*.log.*" -mtime +30 -delete
```

---

## 🔐 Segurança

### Checklist Antes de Deploy

- [ ] `DEBUG = False` no `.env`
- [ ] `SECRET_KEY` forte e única
- [ ] `ALLOWED_HOSTS` configurado corretamente
- [ ] Usar PostgreSQL ao invés de SQLite
- [ ] Habilitar HTTPS
- [ ] Configurar variáveis de segurança
- [ ] Backup regular do banco de dados
- [ ] Monitoramento de logs
- [ ] Rate limiting configurado

---

## 🚀 Deploy

### Preparar para Produção

1. **Configurar Banco PostgreSQL**
```env
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=instalab_production
DATABASE_USER=instalab_user
DATABASE_PASSWORD=senha_forte_aqui
DATABASE_HOST=seu-db-host.com
DATABASE_PORT=5432
```

2. **Configurar Redis**
```env
CACHE_ENABLED=True
REDIS_HOST=seu-redis-host.com
REDIS_PORT=6379
```

3. **Coletar Arquivos Estáticos**
```bash
python manage.py collectstatic --noinput
```

4. **Executar com Gunicorn**
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

---

## 🆘 Troubleshooting

### Erro: "No module named 'environs'"
```bash
pip install environs
```

### Erro: "Table doesn't exist"
```bash
python manage.py migrate
```

### Erro: "SECRET_KEY not set"
```bash
# Gere uma nova key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# Adicione ao .env
echo "SECRET_KEY=sua_key_aqui" >> .env
```

### Erro: Redis connection
```bash
# Certifique-se que Redis está rodando
redis-cli ping
# Ou desabilite cache
echo "CACHE_ENABLED=False" >> .env
```

### Limpar Cache
```bash
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
>>> exit()
```

---

## 📚 Recursos Adicionais

- **Documentação Django**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **Channels**: https://channels.readthedocs.io/
- **PostgreSQL**: https://www.postgresql.org/docs/

---

## 💡 Dicas

1. **Use ambiente virtual sempre**
2. **Nunca commite .env ou SECRET_KEY**
3. **Faça backup regular do banco**
4. **Monitore logs em produção**
5. **Use Redis em produção**
6. **Configure HTTPS**
7. **Implemente rate limiting**
8. **Faça code review antes de merge**

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFeature`)
3. Commit (`git commit -m 'Adiciona NovaFeature'`)
4. Push (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

---

**InstaLab** - Conectando talentos acadêmicos com oportunidades profissionais 🚀
