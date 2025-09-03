# 🐳 Guia Docker Compose - InstaLab

## ✅ PROBLEMA RESOLVIDO!

O Docker Compose agora funciona **exatamente igual** ao ambiente virtual!

### 🎯 Comparação dos ambientes:

| Ambiente | URL | Status |
|----------|-----|--------|
| **Ambiente Virtual** | http://localhost:8001 | ✅ Funcionando perfeitamente |
| **Docker Compose** | http://localhost:8000 | ✅ Funcionando perfeitamente |

### 📋 Como aplicar alterações no Docker:

#### 🔄 **Atualização rápida** (mudanças em CSS/HTML):
```bash
./update_docker.sh
```

#### 🔨 **Rebuild completo** (mudanças em Dockerfile/requirements):
```bash
./update_docker.sh --rebuild
```

#### 🔍 **Helper de desenvolvimento**:
```bash
./dev_helper.sh
```

### �️ Comandos úteis:

- **Ver status dos containers**:
  ```bash
  sudo docker compose ps
  ```

- **Ver logs do container web**:
  ```bash
  sudo docker compose logs web
  ```

- **Parar todos os containers**:
  ```bash
  sudo docker compose down
  ```

- **Iniciar todos os containers**:
  ```bash
  sudo docker compose up -d
  ```

### 🚀 Fluxo de desenvolvimento recomendado:

1. **Desenvolva e teste no ambiente virtual**:
   ```bash
   venv/bin/python manage.py runserver 0.0.0.0:8001
   ```

2. **Quando satisfeito, aplique no Docker**:
   ```bash
   ./update_docker.sh
   ```

3. **Teste no Docker**:
   ```bash
   # Acesse: http://localhost:8000
   ```

### 📱 URLs de acesso:
- **Ambiente Virtual**: http://localhost:8001
- **Docker Compose**: http://localhost:8000
- **Admin Docker**: http://localhost:8000/admin/

### 🎯 Correções aplicadas e funcionando:
- ✅ Header responsivo com zoom funcional
- ✅ Navegação (Home, Login, Cadastro) posicionada corretamente
- ✅ Layout de login otimizado para mobile
- ✅ Media queries para diferentes tamanhos de tela
- ✅ Rebuild automático quando necessário

### 📝 Arquivos importantes:
- `static/css/main.css` - Estilos responsivos
- `apps/core/templates/core/base.html` - Estrutura do header
- `update_docker.sh` - Script de atualização
- `dev_helper.sh` - Helper de desenvolvimento
- `docker-compose.yml` - Configuração Docker (sem version obsoleta)
