# InstaLab

Plataforma social para estudantes, empresas juniores, laboratórios e entusiastas de tecnologia, design, robótica, fotografia e inovação. Objetivo: centralizar projetos, conectar talentos e facilitar colaboração e troca de mensagens em tempo real.

## ✨ Funcionalidades (MVP)

- Cadastro e login (usuário + nickname único + email + senha / confirmar senha)
- Perfil com foto (upload), nickname e bio
- Feed simples de posts (texto / futura imagem)
- Upload de imagens de perfil
- Mensagens em tempo real (WebSocket) via Django Channels (estrutura inicial)
- Pesquisa básica de posts
- Interface minimalista com as cores principais: `#6A5ACD` (Slate Purple) e `#000000`

## 🗺️ Roadmap (Próximas Etapas)

1. Comentários em posts
2. Curtidas / Reações
3. Seguir / Conectar perfis
4. Caixa de entrada (threads de chat) persistente
5. Upload de imagens em posts (galeria) + corte (Pillow)
6. Notificações em tempo real
7. API (Django REST Framework) para apps móveis
8. Deploy (Docker + Gunicorn + Nginx)

## 🛠️ Stack

- Django 4
- Django Channels 4
- Redis (canal de mensagens para produção)
- PostgreSQL (planejado; SQLite em dev inicial)
- Pillow (imagens)
- Crispy Forms (melhor UX de formulários)
- Docker / docker-compose

## 📂 Estrutura Simplificada

```
apps/
  accounts/ (usuários, perfis)
  core/ (posts, feed, pesquisa)
  messaging/ (WebSockets, chat)
config/ (settings, asgi/wsgi)
static/ (css, js, img)
media/ (uploads: profiles, posts)
```

## 🚀 Execução com Docker

```bash
docker compose up --build
```

Acesse: http://localhost:8000

Criar superusuário:

```bash
docker compose run --rm web python manage.py createsuperuser
```

## 🔧 Migrações

```bash
docker compose run --rm web python manage.py makemigrations
docker compose run --rm web python manage.py migrate
```

## 🧪 Testes

```bash
docker compose run --rm web python manage.py test
```

## 📄 Variáveis de Ambiente (.env sugerido)

```
DEBUG=1
SECRET_KEY=alterar_em_producao
ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=social_network
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
REDIS_URL=redis://redis:6379/0
```

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