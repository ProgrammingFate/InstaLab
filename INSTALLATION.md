# ⚠️ Notas Importantes - Pós-Melhorias

## 📦 Instalação de Dependências Necessária

As melhorias adicionaram novas dependências que precisam ser instaladas:

```bash
# Ativar ambiente virtual
source new_venv/bin/activate  # ou venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### Novas Dependências Adicionadas:
- `environs==11.0.0` - Gerenciamento de variáveis de ambiente
- `django-redis==5.4.0` - Cache com Redis
- `djangorestframework-simplejwt==5.3.1` - Autenticação JWT
- `drf-spectacular==0.27.2` - Documentação OpenAPI/Swagger

## 🔧 Configuração Inicial Necessária

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

Mínimo necessário no `.env`:
```env
SECRET_KEY=sua-secret-key-aqui-mude-isso
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

Para gerar uma SECRET_KEY segura:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Criar Diretório de Logs
```bash
mkdir -p logs
```

### 4. Aplicar Migrações (IMPORTANTE!)
As melhorias nos models requerem novas migrações:

```bash
python manage.py makemigrations
python manage.py migrate
```

Isso criará os índices de banco de dados que melhoram a performance.

### 5. (Opcional) Redis para Cache
Se quiser usar cache em desenvolvimento:

```bash
# Instalar Redis
sudo apt-get install redis-server  # Ubuntu/Debian
# ou
brew install redis  # Mac

# Iniciar Redis
redis-server

# Ativar no .env
echo "CACHE_ENABLED=True" >> .env
```

Se não quiser usar Redis agora, deixe `CACHE_ENABLED=False` (padrão).

## ✅ Verificação

Após a configuração, verifique se está tudo OK:

```bash
# Verificar problemas
python manage.py check

# Executar testes
python manage.py test

# Iniciar servidor
python manage.py runserver 8001
```

## 🔴 Erros Comuns e Soluções

### Erro: "Import 'environs' could not be resolved"
**Solução**: Execute `pip install -r requirements.txt`

### Erro: "SECRET_KEY not found"
**Solução**: Crie o arquivo `.env` baseado no `.env.example`

### Erro: "Table doesn't exist"
**Solução**: Execute `python manage.py migrate`

### Erro: "Redis connection failed"
**Solução**: Desabilite cache temporariamente:
```bash
echo "CACHE_ENABLED=False" >> .env
```

### Erro: "ModuleNotFoundError: No module named 'rest_framework'"
**Solução**: Execute `pip install -r requirements.txt`

## 📋 Checklist de Instalação

- [ ] Ativar ambiente virtual
- [ ] `pip install -r requirements.txt`
- [ ] Copiar `.env.example` para `.env`
- [ ] Configurar SECRET_KEY no `.env`
- [ ] Criar diretório `logs/`
- [ ] `python manage.py makemigrations`
- [ ] `python manage.py migrate`
- [ ] `python manage.py check`
- [ ] `python manage.py test` (opcional)
- [ ] `python manage.py runserver 8001`

## 🚀 Ordem de Comandos

Execute na ordem:

```bash
# 1. Ativar ambiente virtual
source new_venv/bin/activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Criar .env
cp .env.example .env

# 4. Gerar SECRET_KEY e adicionar ao .env
python -c "from django.core.management.utils import get_random_secret_key; print('SECRET_KEY=' + get_random_secret_key())" >> .env

# 5. Criar logs
mkdir -p logs

# 6. Migrações
python manage.py makemigrations
python manage.py migrate

# 7. (Opcional) Criar superusuário
python manage.py createsuperuser

# 8. (Opcional) Dados de teste
python scripts/test_data/create_test_users.py

# 9. Verificar
python manage.py check

# 10. Executar
python manage.py runserver 8001
```

## 🎯 Acesso Após Instalação

- **Site**: http://localhost:8001
- **Admin**: http://localhost:8001/admin
- **API Docs**: http://localhost:8001/api/docs/
- **API**: http://localhost:8001/api/v1/

## 📚 Documentação

Consulte os seguintes arquivos para mais informações:

1. **QUICKSTART.md** - Guia rápido de instalação e uso
2. **IMPROVEMENTS.md** - Detalhes técnicos das melhorias
3. **SUMMARY.md** - Resumo executivo das mudanças
4. **README.md** - Documentação geral do projeto

## 🆘 Precisa de Ajuda?

1. Verifique os arquivos de documentação
2. Execute `./manage_helper.sh` para comandos úteis
3. Consulte os logs em `logs/django.log`
4. Abra uma issue no GitHub

## ⚡ Script Rápido

Para facilitar, use o helper:

```bash
chmod +x manage_helper.sh
./manage_helper.sh
```

Ele oferece um menu interativo com as principais operações.

---

**Importante**: Todas as melhorias são **retrocompatíveis**. O código antigo continuará funcionando, mas para aproveitar as novas features (API, cache, índices), siga as instruções acima.

---

Última atualização: 30 de outubro de 2025
