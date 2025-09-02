# 📋 InstaLab - Documentação Completa do Projeto

## 🎯 Visão Geral

**InstaLab** é uma plataforma social inovadora desenvolvida para conectar estudantes, empresas juniores e laboratórios de pesquisa. O sistema oferece uma experiência moderna inspirada no Instagram, com funcionalidades específicas para o ambiente acadêmico e profissional.

---

## 🏗️ Arquitetura do Sistema

### **Stack Tecnológica**
- **Backend**: Django 4.2.9 (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Banco de Dados**: PostgreSQL (produção) / SQLite (desenvolvimento)
- **Cache**: Redis
- **Containerização**: Docker + Docker Compose
- **WebSockets**: Django Channels (para chat em tempo real)

### **Estrutura do Projeto**
```
InstaLab/
├── social_network_project/          # Projeto principal
│   ├── apps/                        # Aplicações Django
│   │   ├── accounts/                # Autenticação e perfis
│   │   ├── core/                    # Funcionalidades centrais
│   │   └── messaging/               # Sistema de mensagens e social
│   ├── config/                      # Configurações Django
│   ├── static/                      # Arquivos estáticos
│   ├── templates/                   # Templates globais
│   └── scripts/                     # Scripts utilitários
└── README.md                        # Documentação do repositório
```

---

## 🚀 Funcionalidades Principais

### **1. Sistema de Usuários** 👥
- **Tipos de Usuário**: Estudantes, Empresas Juniores, Laboratórios
- **Autenticação Completa**: Registro, login, logout
- **Perfis Dinâmicos**: Informações personalizadas por tipo de usuário
- **Campos Específicos**:
  - **Estudantes**: Curso, universidade, semestre, habilidades
  - **Empresas**: Descrição, área de atuação, Instagram
  - **Laboratórios**: Área de pesquisa, projetos

### **2. Sistema de Stories** 📱
**Exclusivo para Empresas e Laboratórios**
- ✨ **Tipos de Story**: Vagas, Projetos, Cultura, Eventos, Conquistas
- ⏰ **Expiração Automática**: 24 horas
- 🎯 **Stories Destacados**: Fixação no topo
- 📊 **Visualizações**: Contadores e registro de quem viu
- 🔗 **Links Externos**: Integração com vagas e projetos

### **3. Área Social dos Estudantes** 🎓
**Rede Social Exclusiva para Estudantes**

#### **Posts Estudantis**
- 🆘 **Pedir Ajuda**: Dúvidas acadêmicas
- 🏆 **Conquistas**: Compartilhar sucessos
- 👥 **Grupos de Estudo**: Organizar estudos colaborativos
- 🤝 **Networking**: Conectar-se com colegas
- 💭 **Discussões**: Debates acadêmicos
- 🏷️ **Sistema de Tags**: Organização e busca
- 🖼️ **Upload de Imagens**: Suporte visual

#### **Grupos de Estudo**
- 📚 **Criação Dinâmica**: Formulário intuitivo
- 🌐 **Tipos de Encontro**: Online, Presencial, Híbrido
- 👥 **Gestão de Membros**: Límites configuráveis
- 🔍 **Filtros Avançados**: Por tipo, matéria, universidade
- ⚡ **Participação Fácil**: Um clique para entrar/sair

#### **Sistema de Conexões**
- 🔍 **Busca Avançada**: Por área, curso, universidade
- 🤝 **Solicitações de Conexão**: Sistema de aprovação
- 📊 **Perfis Detalhados**: Estatísticas de atividade
- 🟢 **Status Online**: Indicadores de presença

### **4. Sistema de Vagas** 💼
- 📝 **Criação de Vagas**: Empresas publicam oportunidades
- 🔍 **Busca Inteligente**: Filtros por categoria, localização
- 📋 **Candidaturas**: Sistema de aplicação simplificado
- 📊 **Gestão de Aplicações**: Dashboard para empresas

### **5. Sistema de Mensagens** 💬
- 💬 **Chat em Tempo Real**: WebSockets com Django Channels
- 👥 **Conversas Privadas**: Entre usuários
- 📱 **Interface Moderna**: Design responsivo
- 🔔 **Notificações**: Sistema de alertas

---

## 🎨 Design e UX

### **Visual Identity**
- 🌈 **Cores Principais**: Gradientes roxos (#6A5ACD, #9370DB)
- 💎 **Glassmorphism**: Efeitos de vidro translúcido
- 📱 **Mobile First**: Design responsivo
- ✨ **Animações Suaves**: Transições e hover effects

### **Componentes UI**
- 🎴 **Cards Glassmórficos**: Containers translúcidos
- 🔘 **Botões Gradiente**: CTAs atraentes
- 📊 **Filtros Visuais**: Tabs e toggles intuitivos
- 🏷️ **Tags Coloridas**: Organização visual
- 🔍 **Busca Avançada**: Múltiplos critérios

---

## 🔧 Configuração e Deploy

### **Requisitos do Sistema**
- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM mínimo
- 10GB espaço livre

### **Instalação Local**
```bash
# 1. Clone o repositório
git clone https://github.com/ProgrammingFate/InstaLab.git
cd InstaLab/social_network_project

# 2. Construir e iniciar containers
sudo docker compose build
sudo docker compose up -d

# 3. Aplicar migrações
sudo docker compose exec web python manage.py migrate

# 4. Criar superusuário (opcional)
sudo docker compose exec web python manage.py createsuperuser

# 5. Popular dados de teste
sudo docker compose exec web python scripts/test_data/create_test_users.py
sudo docker compose exec web python scripts/test_data/populate_social_data.py
```

### **Variáveis de Ambiente**
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@db:5432/social_network
REDIS_URL=redis://redis:6379/0
```

### **Serviços Docker**
- **web**: Django application (porta 8000)
- **db**: PostgreSQL database (porta 5432)
- **redis**: Redis cache (porta 6379)

---

## 📊 Modelos de Dados

### **CustomUser**
```python
- user_type: student/company/lab
- nickname: Nome de exibição
- bio: Biografia
- profile_picture: Foto de perfil
- course: Curso (estudantes)
- university: Universidade
- company_description: Descrição (empresas)
- research_area: Área de pesquisa (labs)
```

### **Story**
```python
- user: Criador (ForeignKey)
- title: Título
- content: Conteúdo
- image: Imagem (opcional)
- story_type: Tipo do story
- expires_at: Data de expiração
- is_highlighted: Destacado
- related_job: Vaga relacionada (opcional)
```

### **StudentPost**
```python
- author: Autor (ForeignKey)
- title: Título
- content: Conteúdo
- post_type: Tipo do post
- tags: Tags (separadas por vírgula)
- image: Imagem (opcional)
- study_subject: Matéria (grupos de estudo)
- max_participants: Máximo de participantes
```

### **StudyGroup**
```python
- creator: Criador (ForeignKey)
- name: Nome do grupo
- subject: Matéria
- description: Descrição
- meeting_type: online/presential/hybrid
- max_members: Limite de membros
- members: Membros (ManyToMany)
- university: Universidade (opcional)
```

---

## 🔐 Segurança e Permissões

### **Controle de Acesso**
- ✅ **Autenticação Obrigatória**: Login necessário
- 🎯 **Permissões por Tipo**: Funcionalidades específicas
- 🛡️ **CSRF Protection**: Tokens em formulários
- 🔒 **Validação de Dados**: Sanitização de inputs

### **Regras de Negócio**
- 📱 **Stories**: Apenas empresas e labs podem criar
- 🎓 **Área Social**: Exclusiva para estudantes
- 💼 **Vagas**: Apenas empresas podem publicar
- 🔗 **Conexões**: Apenas entre estudantes

---

## 📈 Funcionalidades Futuras

### **Roadmap**
- 🔔 **Sistema de Notificações**: Push notifications
- 📧 **E-mail Marketing**: Newsletters automáticas
- 📊 **Analytics**: Dashboard de métricas
- 🤖 **IA Recomendações**: Sugestões personalizadas
- 📱 **App Mobile**: React Native
- 🎥 **Video Stories**: Suporte a vídeos
- 🏆 **Sistema de Badges**: Gamificação
- 📅 **Calendário**: Integração com eventos

---

## 🧪 Testes e Qualidade

### **Dados de Teste Incluídos**
- 👤 **Usuários**: Estudante e empresa exemplo
- 📱 **Stories**: 4 stories de exemplo
- 📝 **Posts**: 5 posts de estudantes
- 👥 **Grupos**: 4 grupos de estudo

### **Credenciais de Teste**
```
Estudante:
- Email: estudante@test.com
- Senha: testpass123

Empresa:
- Email: empresa@test.com  
- Senha: testpass123
```

### **URLs Principais**
- **Home**: http://localhost:8000/
- **Stories**: http://localhost:8000/messaging/stories/
- **Área Social**: http://localhost:8000/messaging/social/
- **Vagas**: http://localhost:8000/vagas/
- **Admin**: http://localhost:8000/admin/

---

## 🤝 Contribuição

### **Como Contribuir**
1. 🍴 Fork o projeto
2. 🌿 Crie uma branch feature
3. 💻 Implemente suas mudanças
4. ✅ Teste as funcionalidades
5. 📝 Commit com mensagens claras
6. 🚀 Envie um Pull Request

### **Padrões de Código**
- 🐍 **PEP 8**: Estilo Python
- 📝 **Docstrings**: Documentação em funções
- 🧪 **Testes**: Cobertura mínima de 80%
- 🔄 **Git Flow**: Branches organizadas

---

## 📞 Suporte

### **Contato**
- 📧 **Email**: support@instalab.com
- 💬 **Issues**: GitHub Issues
- 📖 **Wiki**: Documentação detalhada
- 🤝 **Community**: Discord/Slack

### **Troubleshooting**
- 🐳 **Docker Issues**: Verificar logs dos containers
- 🗄️ **Database**: Reset com `docker compose down -v`
- 🔄 **Rebuild**: `docker compose build --no-cache`
- 📊 **Logs**: `docker compose logs web`

---

## 📜 Licença

**MIT License** - Livre para uso comercial e pessoal.

---

## 🎉 Agradecimentos

Desenvolvido com ❤️ pela equipe InstaLab.
Obrigado a todos os contribuidores e testadores que tornaram este projeto possível!

---

**InstaLab v1.0** - Conectando o futuro acadêmico! 🚀
