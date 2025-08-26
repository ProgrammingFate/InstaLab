# InstaLab

Plataforma de vagas e estágios para estudantes, empresas e laboratórios de tecnologia, design, robótica, fotografia e inovação. Conecta talentos acadêmicos com oportunidades profissionais de forma simples e eficiente.

## ✨ Funcionalidades Principais

- **Sistema de Usuários Diferenciados**: Cadastro como Estudante ou Empresa
- **Gestão de Vagas**: Empresas podem criar, editar e gerenciar suas vagas
- **Aplicação a Vagas**: Estudantes podem se candidatar às oportunidades
- **Perfis Completos**: Upload de foto, bio e informações da empresa/estudante
- **Categorização**: Vagas organizadas por categorias (Tecnologia, Design, etc.)
- **Busca e Filtros**: Sistema de pesquisa por título, categoria e localização
- **Dashboard Personalizado**: Visualização das candidaturas e vagas criadas
- **Interface Moderna**: Design inspirado no Instagram com glassmorphism

## 🎯 Tipos de Usuário

- **Estudantes**: Podem navegar, pesquisar e se candidatar a vagas
- **Empresas**: Podem criar vagas, gerenciar candidaturas e visualizar perfis dos candidatos

## 🗺️ Roadmap (Próximas Etapas)

1. Sistema de mensagens entre empresas e candidatos
2. Notificações em tempo real
3. Upload de currículos (PDF)
4. Sistema de avaliação de candidatos
5. Relatórios e analytics para empresas
6. API REST para aplicações móveis
7. Sistema de recomendações
8. Deploy em produção

## 🛠️ Stack Tecnológica

- **Backend**: Django 4.2.9
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Upload de Arquivos**: Pillow para processamento de imagens
- **Frontend**: HTML5, CSS3 com Glassmorphism, JavaScript
- **Autenticação**: Sistema customizado com tipos de usuário
- **Deploy**: Docker / docker-compose (configurado)

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

### Desenvolvimento Local

```bash
# Clone o repositório
git clone https://github.com/ProgrammingFate/InstaLab.git
cd InstaLab/social_network_project

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações
python manage.py migrate

# Crie dados de teste (opcional)
python create_test_users.py
python populate_jobs.py

# Execute o servidor
python manage.py runserver 8001
```

### Com Docker

```bash
docker compose up --build
```

Acesse: http://localhost:8001

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

## � Funcionalidades Implementadas

- ✅ Sistema de autenticação diferenciado (Estudante/Empresa)
- ✅ CRUD completo de vagas
- ✅ Sistema de candidaturas
- ✅ Upload de fotos de perfil
- ✅ Busca e filtros por categoria/localização
- ✅ Dashboard para empresas e estudantes
- ✅ Interface responsiva com design moderno
- ✅ Paginação de resultados
- ✅ Gestão de status de candidaturas

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