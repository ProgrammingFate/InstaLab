# 🔌 Exemplos de Uso da API - InstaLab

## 📋 Índice

1. [Autenticação](#autenticação)
2. [Usuários](#usuários)
3. [Posts](#posts)
4. [Vagas](#vagas)
5. [Candidaturas](#candidaturas)
6. [Exemplos com Python](#exemplos-com-python)
7. [Exemplos com JavaScript](#exemplos-com-javascript)

---

## 🔐 Autenticação

### Obter Token JWT

```bash
curl -X POST http://localhost:8001/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "seu_usuario",
    "password": "sua_senha"
  }'
```

**Resposta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Renovar Token

```bash
curl -X POST http://localhost:8001/api/v1/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "SEU_REFRESH_TOKEN"
  }'
```

**Resposta:**
```json
{
  "access": "novo_access_token..."
}
```

---

## 👤 Usuários

### Listar Usuários

```bash
curl http://localhost:8001/api/v1/users/ \
  -H "Authorization: Bearer SEU_TOKEN"
```

### Buscar Usuário

```bash
curl "http://localhost:8001/api/v1/users/?search=nome" \
  -H "Authorization: Bearer SEU_TOKEN"
```

### Meu Perfil

```bash
curl http://localhost:8001/api/v1/users/me/ \
  -H "Authorization: Bearer SEU_TOKEN"
```

**Resposta:**
```json
{
  "id": 1,
  "username": "joao_estudante",
  "nickname": "João Silva",
  "email": "joao@email.com",
  "user_type": "student",
  "bio": "Estudante de Engenharia",
  "course": "Engenharia de Software",
  "university": "UFSC",
  "semester": "5"
}
```

---

## 📱 Posts

### Listar Posts do Feed

```bash
curl "http://localhost:8001/api/v1/posts/?feed=true" \
  -H "Authorization: Bearer SEU_TOKEN"
```

### Criar Post

```bash
curl -X POST http://localhost:8001/api/v1/posts/ \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Meu novo post sobre tecnologia!",
    "post_type": "text",
    "hashtags": "tecnologia, programação, python",
    "location": "Florianópolis, SC"
  }'
```

### Criar Post com Imagem

```bash
curl -X POST http://localhost:8001/api/v1/posts/ \
  -H "Authorization: Bearer SEU_TOKEN" \
  -F "content=Veja essa foto incrível!" \
  -F "post_type=photo" \
  -F "image=@/caminho/para/imagem.jpg"
```

### Ver Detalhes do Post

```bash
curl http://localhost:8001/api/v1/posts/1/ \
  -H "Authorization: Bearer SEU_TOKEN"
```

**Resposta:**
```json
{
  "id": 1,
  "author": {
    "id": 1,
    "username": "joao_estudante",
    "nickname": "João Silva",
    "avatar": "/media/avatars/joao.jpg",
    "user_type": "student"
  },
  "content": "Meu novo post sobre tecnologia!",
  "image": null,
  "video": null,
  "post_type": "text",
  "created_at": "2025-10-30T10:30:00Z",
  "location": "Florianópolis, SC",
  "hashtags": "tecnologia, programação, python",
  "likes_count": 15,
  "comments_count": 3,
  "user_liked": false
}
```

### Curtir/Descurtir Post

```bash
curl -X POST http://localhost:8001/api/v1/posts/1/like/ \
  -H "Authorization: Bearer SEU_TOKEN"
```

**Resposta:**
```json
{
  "liked": true,
  "likes_count": 16
}
```

### Comentar em Post

```bash
curl -X POST http://localhost:8001/api/v1/posts/1/comment/ \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Ótimo post! Adorei."
  }'
```

### Ver Comentários do Post

```bash
curl http://localhost:8001/api/v1/posts/1/comments/ \
  -H "Authorization: Bearer SEU_TOKEN"
```

### Filtrar Posts por Tipo

```bash
curl "http://localhost:8001/api/v1/posts/?post_type=photo" \
  -H "Authorization: Bearer SEU_TOKEN"
```

### Buscar Posts

```bash
curl "http://localhost:8001/api/v1/posts/?search=tecnologia" \
  -H "Authorization: Bearer SEU_TOKEN"
```

---

## 💼 Vagas

### Listar Vagas Ativas

```bash
curl http://localhost:8001/api/v1/jobs/ \
  -H "Authorization: Bearer SEU_TOKEN"
```

### Filtrar por Categoria

```bash
curl "http://localhost:8001/api/v1/jobs/?category=1" \
  -H "Authorization: Bearer SEU_TOKEN"
```

### Filtrar por Tipo e Localização

```bash
curl "http://localhost:8001/api/v1/jobs/?job_type=internship&location=São Paulo" \
  -H "Authorization: Bearer SEU_TOKEN"
```

### Buscar Vagas

```bash
curl "http://localhost:8001/api/v1/jobs/?search=desenvolvedor python" \
  -H "Authorization: Bearer SEU_TOKEN"
```

### Criar Vaga (Apenas Empresas)

```bash
curl -X POST http://localhost:8001/api/v1/jobs/ \
  -H "Authorization: Bearer SEU_TOKEN_EMPRESA" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Desenvolvedor Python Júnior",
    "description": "Buscamos desenvolvedor Python com conhecimento em Django...",
    "requirements": "- Python 3.x\n- Django\n- Git\n- SQL",
    "benefits": "- Vale alimentação\n- Home office",
    "job_type": "full_time",
    "experience_level": "junior",
    "location": "São Paulo, SP",
    "salary_range": "R$ 3.000 - R$ 5.000",
    "tags": "python, django, backend, web"
  }'
```

**Resposta:**
```json
{
  "id": 10,
  "company": {
    "id": 5,
    "username": "techjr",
    "nickname": "TechJr Empresa",
    "user_type": "company"
  },
  "title": "Desenvolvedor Python Júnior",
  "category": null,
  "description": "Buscamos desenvolvedor Python...",
  "job_type": "full_time",
  "experience_level": "junior",
  "location": "São Paulo, SP",
  "status": "active",
  "created_at": "2025-10-30T10:30:00Z",
  "applications_count": 0,
  "is_applied": false
}
```

### Ver Detalhes da Vaga

```bash
curl http://localhost:8001/api/v1/jobs/10/ \
  -H "Authorization: Bearer SEU_TOKEN"
```

### Minhas Vagas (Para Empresas)

```bash
curl "http://localhost:8001/api/v1/jobs/?my_jobs=true" \
  -H "Authorization: Bearer SEU_TOKEN_EMPRESA"
```

---

## 📝 Candidaturas

### Candidatar-se a uma Vaga

```bash
curl -X POST http://localhost:8001/api/v1/jobs/10/apply/ \
  -H "Authorization: Bearer SEU_TOKEN_ESTUDANTE" \
  -H "Content-Type: application/json" \
  -d '{
    "cover_letter": "Prezados, tenho grande interesse nesta vaga pois possuo experiência com Python e Django. Durante meu curso aprendi..."
  }'
```

### Candidatar-se com Currículo

```bash
curl -X POST http://localhost:8001/api/v1/jobs/10/apply/ \
  -H "Authorization: Bearer SEU_TOKEN_ESTUDANTE" \
  -F "cover_letter=Prezados, tenho grande interesse..." \
  -F "resume=@/caminho/para/curriculo.pdf"
```

### Minhas Candidaturas

```bash
curl http://localhost:8001/api/v1/applications/ \
  -H "Authorization: Bearer SEU_TOKEN_ESTUDANTE"
```

**Resposta:**
```json
[
  {
    "id": 1,
    "job": {
      "id": 10,
      "title": "Desenvolvedor Python Júnior",
      "company": {...}
    },
    "applicant": {...},
    "cover_letter": "Prezados...",
    "status": "pending",
    "applied_at": "2025-10-30T10:30:00Z"
  }
]
```

### Ver Candidaturas de uma Vaga (Empresa)

```bash
curl http://localhost:8001/api/v1/jobs/10/applications/ \
  -H "Authorization: Bearer SEU_TOKEN_EMPRESA"
```

### Atualizar Status da Candidatura (Empresa)

```bash
curl -X PATCH http://localhost:8001/api/v1/applications/1/update_status/ \
  -H "Authorization: Bearer SEU_TOKEN_EMPRESA" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "interview",
    "company_notes": "Candidato selecionado para entrevista."
  }'
```

---

## 🐍 Exemplos com Python

### Setup Inicial

```python
import requests

BASE_URL = "http://localhost:8001/api/v1"

class InstaLabAPI:
    def __init__(self, username, password):
        self.base_url = BASE_URL
        self.token = None
        self.refresh_token = None
        self.login(username, password)
    
    def login(self, username, password):
        """Autenticar e obter token"""
        response = requests.post(
            f"{self.base_url}/auth/token/",
            json={"username": username, "password": password}
        )
        data = response.json()
        self.token = data["access"]
        self.refresh_token = data["refresh"]
    
    def get_headers(self):
        """Retornar headers com autenticação"""
        return {"Authorization": f"Bearer {self.token}"}
    
    def refresh_access_token(self):
        """Renovar token de acesso"""
        response = requests.post(
            f"{self.base_url}/auth/token/refresh/",
            json={"refresh": self.refresh_token}
        )
        self.token = response.json()["access"]
```

### Listar Posts

```python
api = InstaLabAPI("seu_usuario", "sua_senha")

# Listar posts do feed
response = requests.get(
    f"{BASE_URL}/posts/?feed=true",
    headers=api.get_headers()
)
posts = response.json()

for post in posts["results"]:
    print(f"Post por {post['author']['username']}: {post['content']}")
```

### Criar Post

```python
# Criar post de texto
response = requests.post(
    f"{BASE_URL}/posts/",
    headers=api.get_headers(),
    json={
        "content": "Meu post via API!",
        "post_type": "text",
        "hashtags": "api, python, django"
    }
)
new_post = response.json()
print(f"Post criado com ID: {new_post['id']}")
```

### Candidatar-se a Vaga

```python
# Buscar vagas
response = requests.get(
    f"{BASE_URL}/jobs/?search=python",
    headers=api.get_headers()
)
jobs = response.json()["results"]

# Candidatar-se à primeira vaga
if jobs:
    job_id = jobs[0]["id"]
    response = requests.post(
        f"{BASE_URL}/jobs/{job_id}/apply/",
        headers=api.get_headers(),
        json={
            "cover_letter": "Tenho interesse nesta vaga porque..."
        }
    )
    if response.status_code == 201:
        print("Candidatura enviada com sucesso!")
```

---

## 🌐 Exemplos com JavaScript

### Setup com Fetch API

```javascript
class InstaLabAPI {
  constructor(baseUrl = 'http://localhost:8001/api/v1') {
    this.baseUrl = baseUrl;
    this.token = null;
  }

  async login(username, password) {
    const response = await fetch(`${this.baseUrl}/auth/token/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    this.token = data.access;
    this.refreshToken = data.refresh;
    return data;
  }

  getHeaders() {
    return {
      'Authorization': `Bearer ${this.token}`,
      'Content-Type': 'application/json'
    };
  }

  async get(endpoint) {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      headers: this.getHeaders()
    });
    return response.json();
  }

  async post(endpoint, data) {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(data)
    });
    return response.json();
  }
}
```

### Usar a API

```javascript
// Inicializar
const api = new InstaLabAPI();
await api.login('seu_usuario', 'sua_senha');

// Listar posts
const posts = await api.get('/posts/?feed=true');
console.log(posts);

// Criar post
const newPost = await api.post('/posts/', {
  content: 'Post via JavaScript!',
  post_type: 'text'
});
console.log('Post criado:', newPost);

// Curtir post
const like = await api.post(`/posts/${newPost.id}/like/`, {});
console.log('Post curtido!', like);

// Listar vagas
const jobs = await api.get('/jobs/');
console.log('Vagas disponíveis:', jobs.results);
```

### Com Axios

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8001/api/v1',
});

// Interceptor para adicionar token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Login
const login = async (username, password) => {
  const response = await api.post('/auth/token/', { username, password });
  localStorage.setItem('access_token', response.data.access);
  localStorage.setItem('refresh_token', response.data.refresh);
  return response.data;
};

// Listar posts
const getPosts = async () => {
  const response = await api.get('/posts/?feed=true');
  return response.data;
};

// Criar post
const createPost = async (content, postType = 'text') => {
  const response = await api.post('/posts/', {
    content,
    post_type: postType
  });
  return response.data;
};
```

---

## 📊 Paginação

Todas as listagens suportam paginação:

```bash
curl "http://localhost:8001/api/v1/posts/?page=2&page_size=20" \
  -H "Authorization: Bearer SEU_TOKEN"
```

**Resposta:**
```json
{
  "count": 100,
  "next": "http://localhost:8001/api/v1/posts/?page=3",
  "previous": "http://localhost:8001/api/v1/posts/?page=1",
  "results": [...]
}
```

---

## 🔍 Filtros Avançados

### Posts

```bash
# Feed + busca + tipo
curl "http://localhost:8001/api/v1/posts/?feed=true&search=python&post_type=text" \
  -H "Authorization: Bearer SEU_TOKEN"
```

### Vagas

```bash
# Múltiplos filtros
curl "http://localhost:8001/api/v1/jobs/?category=1&job_type=internship&experience_level=entry&search=python&location=São Paulo" \
  -H "Authorization: Bearer SEU_TOKEN"
```

---

## 📱 App Móvel Exemplo (React Native)

```javascript
// services/api.js
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API = axios.create({
  baseURL: 'https://seudominio.com/api/v1',
});

API.interceptors.request.use(async config => {
  const token = await AsyncStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = async (username, password) => {
  const { data } = await API.post('/auth/token/', { username, password });
  await AsyncStorage.setItem('access_token', data.access);
  await AsyncStorage.setItem('refresh_token', data.refresh);
  return data;
};

export const getFeed = () => API.get('/posts/?feed=true');
export const likePost = (postId) => API.post(`/posts/${postId}/like/`);
export const getJobs = (params) => API.get('/jobs/', { params });
export const applyToJob = (jobId, coverLetter) => 
  API.post(`/jobs/${jobId}/apply/`, { cover_letter: coverLetter });
```

---

## 🎯 Documentação Interativa

Acesse a documentação Swagger completa em:
**http://localhost:8001/api/docs/**

Lá você pode:
- Ver todos os endpoints
- Testar requisições diretamente
- Ver schemas de request/response
- Gerar código em várias linguagens

---

## 📞 Suporte

Para mais exemplos e dúvidas:
1. Consulte a documentação Swagger
2. Veja o código em `apps/api/`
3. Abra uma issue no GitHub

---

**InstaLab API** - Conectando talentos via API 🚀
