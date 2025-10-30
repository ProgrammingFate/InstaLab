# InstaLab

Plataforma de vagas e estágios para estudantes, empresas e laboratórios de tecnologia, design, robótica, fotografia e inovação. Conecta talentos acadêmicos com oportunidades profissionais de forma simples e eficiente.

## ✨ Funcionalidades Principais

### 💼 Sistema de Vagas
- **Sistema de Usuários Diferenciados**: Cadastro como Estudante ou Empresa
- **Gestão de Vagas**: Empresas podem criar, editar e gerenciar suas vagas
- **Aplicação a Vagas**: Estudantes podem se candidatar às oportunidades
- **Perfis Completos**: Upload de foto, bio e informações da empresa/estudante
- **Categorização**: Vagas organizadas por categorias (Tecnologia, Design, etc.)
- **Busca e Filtros**: Sistema de pesquisa por título, categoria e localização
- **Dashboard Personalizado**: Visualização das candidaturas e vagas criadas

### 📱 Rede Social
- **Feed Estilo Instagram**: Posts com fotos, vídeos e textos
- **Stories**: Conteúdo temporário (24 horas)
- **Likes e Comentários**: Interação social completa
- **Seguir Usuários**: Sistema de follows
- **Interface Moderna**: Design inspirado no Instagram com glassmorphism

### 🔌 API REST
- **Autenticação JWT**: Segura e moderna
- **Documentação Swagger**: Interativa e completa
- **Endpoints Completos**: Posts, Vagas, Candidaturas, Usuários
- **Pronto para Mobile**: Aplicações móveis podem consumir a API

## 🎯 Tipos de Usuário

- **Estudantes**: Podem navegar, pesquisar e se candidatar a vagas
- **Empresas**: Podem criar vagas, gerenciar candidaturas e visualizar perfis dos candidatos

## 🎉 Novidades v2.0

### ✅ Recém Implementado
- ✅ **API REST Completa** com Django REST Framework
- ✅ **Autenticação JWT** para segurança
- ✅ **Documentação Swagger** interativa
- ✅ **Sistema de Cache** com Redis
- ✅ **Logging Estruturado** para monitoramento
- ✅ **Otimização de Performance** (índices de DB)
- ✅ **Testes Automatizados** (50+ testes)
- ✅ **Variáveis de Ambiente** para segurança
- ✅ **Tratamento Robusto de Erros**
- ✅ **Validações Completas** nos models

### 📚 Nova Documentação
- 📖 `IMPROVEMENTS.md` - Detalhes técnicos das melhorias
- 🚀 `QUICKSTART.md` - Guia rápido de instalação
- 📊 `SUMMARY.md` - Resumo executivo
- 🔌 `API_EXAMPLES.md` - Exemplos de uso da API
- ⚙️ `INSTALLATION.md` - Guia de instalação detalhado

## 🗺️ Roadmap (Próximas Etapas)

1. ~~API REST para aplicações móveis~~ ✅ **CONCLUÍDO**
2. Sistema de mensagens entre empresas e candidatos
3. Notificações em tempo real via WebSocket
4. Upload de currículos (PDF) com parser
5. Sistema de avaliação de candidatos
6. Relatórios e analytics para empresas
7. Sistema de recomendações com ML
8. Deploy em produção
9. CI/CD com GitHub Actions
10. App móvel (React Native)

## 🛠️ Stack Tecnológica

### Backend
- **Django 4.2.9** - Framework web
- **Django REST Framework 3.14** - API REST
- **Channels 4.0** - WebSocket support
- **PostgreSQL / SQLite** - Banco de dados
- **Redis** - Cache e Channels

### APIs & Integrações
- **JWT** - Autenticação segura
- **drf-spectacular** - Documentação OpenAPI/Swagger
- **django-filter** - Filtros avançados

### Frontend
- **HTML5, CSS3** com Glassmorphism
- **JavaScript** vanilla
- **Bootstrap 5** (customizado)

### DevOps
- **Docker & docker-compose** - Containerização
- **Gunicorn** - WSGI server
- **WhiteNoise** - Static files
- **Logging rotativo** - Monitoramento

## 📂 Estrutura do Projeto

```
apps/
  accounts/ (autenticação, perfis de usuário)
  core/ (vagas, candidaturas, dashboard)
  messaging/ (sistema de mensagens - futuro)
config/ (configurações Django)
static/ (CSS, JS, imagens, favicon)
media/ (uploads de perfis)
templates/ (templates HTML)
```

## 🚀 Como Executar

### 📖 Guias Disponíveis
- 🚀 **QUICKSTART.md** - Guia rápido
- ⚙️ **INSTALLATION.md** - Instalação detalhada
- 🔌 **API_EXAMPLES.md** - Exemplos da API

### Desenvolvimento Local (Rápido)

```bash
# 1. Clone o repositório
git clone https://github.com/ProgrammingFate/InstaLab.git
cd InstaLab/social_network_project

# 2. Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações

# 5. Crie diretório de logs
mkdir logs

# 6. Execute migrações
python manage.py makemigrations
python manage.py migrate

# 7. (Opcional) Crie superusuário
python manage.py createsuperuser

# 8. (Opcional) Dados de teste
python scripts/test_data/create_test_users.py

# 9. Execute o servidor
python manage.py runserver 8001
```

### Usando Script Helper

```bash
chmod +x manage_helper.sh
./manage_helper.sh  # Menu interativo
```

### Com Docker

```bash
docker compose up --build
```

### 🌐 Acesso

- **Site**: http://localhost:8001
- **Admin**: http://localhost:8001/admin
- **API**: http://localhost:8001/api/v1/
- **API Docs (Swagger)**: http://localhost:8001/api/docs/

## 👤 Usuários de Teste

- **Estudante**: `joao_estudante` / senha: `senha123`
- **Empresa**: `techjr` / senha: `senha123`

## 🎨 Design System

- **Cor Principal**: `#6A5ACD` (Slate Purple)
- **Cores Secundárias**: Gradientes e glassmorphism
- **Tipografia**: Roboto, sans-serif
- **Estilo**: Moderno, limpo, inspirado em redes sociais

## 🔧 Comandos Úteis

### Migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### Criar Superusuário
```bash
python manage.py createsuperuser
```

### Executar Testes
```bash
python manage.py test
```

### Com Docker
```bash
docker compose run --rm web python manage.py createsuperuser
docker compose run --rm web python manage.py test
```

## ✅ Funcionalidades Implementadas

### Core Features
- ✅ Sistema de autenticação diferenciado (Estudante/Empresa)
- ✅ CRUD completo de vagas
- ✅ Sistema de candidaturas
- ✅ Upload de fotos de perfil
- ✅ Busca e filtros por categoria/localização
- ✅ Dashboard para empresas e estudantes
- ✅ Interface responsiva com design moderno
- ✅ Paginação de resultados
- ✅ Gestão de status de candidaturas

### Rede Social
- ✅ Feed estilo Instagram
- ✅ Posts (foto, vídeo, texto)
- ✅ Stories temporários (24h)
- ✅ Likes e comentários
- ✅ Sistema de follows
- ✅ Hashtags

### API & Performance
- ✅ API REST completa
- ✅ Autenticação JWT
- ✅ Documentação Swagger
- ✅ Cache com Redis
- ✅ Índices de banco de dados
- ✅ Query optimization

### Qualidade & Segurança
- ✅ 50+ testes automatizados
- ✅ Logging estruturado
- ✅ Tratamento robusto de erros
- ✅ Validações completas
- ✅ Variáveis de ambiente
- ✅ Configurações de segurança

## 🎯 Casos de Uso

1. **Para Estudantes**:
   - Cadastro com informações acadêmicas
   - Navegação e busca de vagas
   - Candidatura a oportunidades
   - Acompanhamento de candidaturas

2. **Para Empresas**:
   - Cadastro com informações corporativas
   - Criação e gestão de vagas
   - Visualização de candidatos
   - Gestão de candidaturas recebidas

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 🛡️ Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**InstaLab** - Conectando talentos acadêmicos com oportunidades profissionais 🚀

## 🎨 Estilo

Use `#6A5ACD` para elementos de destaque (links, botões primários) e `#000000` / tons de cinza para tipografia e fundo. Manter UI limpa e focada no conteúdo (projetos e perfis).

## 🧱 Próximas Melhorias Técnicas

- Trocar InMemoryChannelLayer por Redis em produção
- Servir arquivos estáticos com Nginx
- Implementar storage S3 opcional
- Indexação de busca (PostgreSQL trigram / Elastic opcional)

## 🤝 Contribuição

Pull requests são bem-vindos. Abrir issues para sugestões.

## 🛡️ Licença

MIT - ver `LICENSE`.

---

Feito para a comunidade acadêmica e criativa. Construído com Django.
