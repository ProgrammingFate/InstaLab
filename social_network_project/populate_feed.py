#!/usr/bin/env python
"""
Script para popular o feed do InstaLab com dados de teste
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.core.models import Post, Like, Comment, Follow, Story
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()

def create_users():
    """Criar usuários de teste"""
    print("🔷 Criando usuários...")
    
    users_data = [
        {
            'username': 'techjr_company',
            'email': 'contato@techjr.com',
            'first_name': 'Tech',
            'last_name': 'Junior',
            'user_type': 'company',
            'company_name': 'Tech Jr - Empresa Junior',
            'company_description': 'Empresa Junior de Tecnologia focada em desenvolvimento web e mobile.',
            'bio': 'Transformando ideias em soluções digitais 💻'
        },
        {
            'username': 'ai_lab_usp',
            'email': 'contato@ailab.usp.br',
            'first_name': 'AI Lab',
            'last_name': 'USP',
            'user_type': 'company',
            'company_name': 'Laboratório de IA - USP',
            'company_description': 'Pesquisa de ponta em Machine Learning e Deep Learning',
            'bio': 'Desenvolvendo o futuro da IA 🤖'
        },
        {
            'username': 'startup_tech',
            'email': 'contato@startuptech.com',
            'first_name': 'Startup',
            'last_name': 'Tech',
            'user_type': 'company',
            'company_name': 'Startup Inovação',
            'company_description': 'Startup inovadora criando soluções tecnológicas disruptivas',
            'bio': 'Do MVP ao scale-up 🚀'
        },
        {
            'username': 'joao_dev',
            'email': 'joao@email.com',
            'first_name': 'João',
            'last_name': 'Silva',
            'user_type': 'student',
            'bio': 'Desenvolvedor Full Stack | React & Node.js'
        },
        {
            'username': 'maria_data',
            'email': 'maria@email.com',
            'first_name': 'Maria',
            'last_name': 'Santos',
            'user_type': 'student',
            'bio': 'Data Scientist | Python & Machine Learning'
        },
        {
            'username': 'pedro_mobile',
            'email': 'pedro@email.com',
            'first_name': 'Pedro',
            'last_name': 'Costa',
            'user_type': 'student',
            'bio': 'Mobile Developer | Flutter & React Native'
        }
    ]
    
    created_users = {}
    for user_data in users_data:
        username = user_data['username']
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=user_data['email'],
                password='teste123',
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                user_type=user_data['user_type'],
                nickname=username  # Adicionar nickname
            )
            
            # Adicionar campos extras
            if 'company_name' in user_data:
                user.company_name = user_data['company_name']
            if 'company_description' in user_data:
                user.company_description = user_data['company_description']
            if 'bio' in user_data:
                user.bio = user_data['bio']
            
            user.save()
            created_users[username] = user
            print(f"  ✅ Criado: {username}")
        else:
            created_users[username] = User.objects.get(username=username)
            print(f"  ⏭️  Já existe: {username}")
    
    return created_users


def create_posts(users):
    """Criar posts de teste"""
    print("\n📝 Criando posts...")
    
    posts_data = [
        {
            'author': 'techjr_company',
            'content': '''🚀 Nova vaga aberta! Estamos procurando um desenvolvedor Frontend Jr para nossa equipe.

💼 Requisitos:
• React.js e JavaScript
• CSS3 e HTML5
• Git/GitHub

💰 Bolsa: R$ 800-1200
📍 Remoto/Híbrido

Interessados, enviem CV para: vagas@techjr.com

#VagaAberta #Frontend #ReactJS #EmpreseJunior #Oportunidade''',
        },
        {
            'author': 'ai_lab_usp',
            'content': '''🤖 Oportunidade de Iniciação Científica em IA!

🔬 Área: Machine Learning aplicado à Visão Computacional

📋 O que você vai aprender:
• Python e TensorFlow
• Redes Neurais Profundas  
• Processamento de Imagens
• Metodologia Científica

💰 Bolsa CNPq disponível
📧 Envie seu CV para: ai.lab@usp.br

#IA #MachineLearning #IniciacaoCientifica #USP #CNPq''',
        },
        {
            'author': 'startup_tech',
            'content': '''🚀 Vem fazer parte da nossa equipe!

📱 Posições disponíveis:
• Desenvolvedor Backend (Node.js/Python)
• Desenvolvedor Mobile (React Native)

🎯 Oferecemos:
• Ambiente jovem e dinâmico
• Mentoria técnica
• Flexibilidade de horários
• Vale refeição + transporte

💡 Trabalhamos com soluções inovadoras para educação

Candidate-se em: www.startuptech.com/vagas

#Startup #Backend #Mobile #ReactNative #NodeJS #Estágio''',
        },
        {
            'author': 'techjr_company',
            'content': '''📢 Workshop de React.js neste sábado!

🗓️ Data: Sábado, 14h
📍 Local: Online (link no bio)

Vamos abordar:
• Hooks e Context API
• Performance e otimizações
• Boas práticas
• Projeto prático

Vagas limitadas! Inscreva-se já 👉 link na bio

#Workshop #ReactJS #Frontend #Aprendizado''',
        },
        {
            'author': 'ai_lab_usp',
            'content': '''🎓 Nosso artigo sobre Deep Learning foi aceito na conferência internacional CVPR 2025!

Trabalho sobre reconhecimento de objetos em tempo real usando redes neurais convolucionais.

Parabéns a toda equipe! 🎉

#Pesquisa #DeepLearning #ComputerVision #USP #CVPR''',
        },
        {
            'author': 'joao_dev',
            'content': '''Finalmente terminei meu projeto pessoal! 🎉

Um app de gerenciamento de tarefas com React e Node.js, usando MongoDB e autenticação JWT.

Foi desafiador mas aprendi muito! 💪

Repo no GitHub: github.com/joaodev/taskapp

#React #NodeJS #FullStack #ProjetoPessoal''',
        },
        {
            'author': 'maria_data',
            'content': '''📊 Análise de dados interessante que fiz hoje!

Descobri padrões fascinantes no dataset de vendas usando Python e Pandas.

A visualização com Seaborn ficou incrível! 📈

#DataScience #Python #Analytics #MachineLearning''',
        },
        {
            'author': 'pedro_mobile',
            'content': '''Acabei de publicar meu primeiro app na Play Store! 🎉📱

Um app de receitas com Flutter que estou desenvolvendo há 3 meses.

Baixem e me deem feedback! Link na bio 👆

#Flutter #Mobile #Android #AppDevelopment''',
        },
        {
            'author': 'startup_tech',
            'content': '''🎯 Milestone alcançado: 10.000 usuários! 🎉

Muito obrigado a todos que acreditaram na nossa solução desde o início.

Isso é só o começo! 🚀

#Startup #Milestone #Crescimento #Agradecimento''',
        },
        {
            'author': 'techjr_company',
            'content': '''💡 Dica do dia: Como organizar seu código React

1️⃣ Use componentes funcionais
2️⃣ Separe lógica de apresentação
3️⃣ Crie hooks customizados
4️⃣ Mantenha componentes pequenos
5️⃣ Use TypeScript sempre que possível

Qual sua melhor prática? Comenta aí! 👇

#React #BestPractices #CleanCode #Frontend''',
        },
    ]
    
    created_posts = []
    for post_data in posts_data:
        author = users.get(post_data['author'])
        if author:
            post = Post.objects.create(
                author=author,
                content=post_data['content'],
                is_active=True
            )
            created_posts.append(post)
            print(f"  ✅ Post criado por {author.username}")
    
    return created_posts


def create_follows(users):
    """Criar relacionamentos de seguir"""
    print("\n👥 Criando follows...")
    
    students = [u for u in users.values() if u.user_type == 'student']
    companies = [u for u in users.values() if u.user_type == 'company']
    
    # Estudantes seguem empresas
    for student in students:
        for company in companies:
            Follow.objects.get_or_create(
                follower=student,
                following=company
            )
        print(f"  ✅ {student.username} seguindo empresas")
    
    # Estudantes se seguem mutuamente
    for i, student1 in enumerate(students):
        for student2 in students[i+1:]:
            Follow.objects.get_or_create(
                follower=student1,
                following=student2
            )
            Follow.objects.get_or_create(
                follower=student2,
                following=student1
            )
    
    print(f"  ✅ Total de {Follow.objects.count()} follows criados")


def create_likes(users, posts):
    """Criar likes nos posts"""
    print("\n❤️  Criando likes...")
    
    students = [u for u in users.values() if u.user_type == 'student']
    
    for post in posts:
        # 2-3 likes por post
        num_likes = random.randint(2, min(3, len(students)))
        likers = random.sample(students, num_likes)
        
        for liker in likers:
            Like.objects.get_or_create(
                user=liker,
                post=post
            )
    
    print(f"  ✅ Total de {Like.objects.count()} likes criados")


def create_comments(users, posts):
    """Criar comentários nos posts"""
    print("\n💬 Criando comentários...")
    
    comments_templates = [
        "Muito interessante! 👏",
        "Ótima iniciativa!",
        "Adorei a ideia! 💡",
        "Parabéns pelo trabalho!",
        "Quando começa? Quero participar!",
        "Excelente! Já me inscrevi 🎉",
        "Que legal! Vou me candidatar",
        "Top demais! 🚀",
        "Muito bom! Continue assim!",
        "Incrível! 😍",
    ]
    
    students = [u for u in users.values() if u.user_type == 'student']
    
    for post in posts[:6]:  # Comentários nos primeiros 6 posts
        # 1-2 comentários por post
        num_comments = random.randint(1, 2)
        commenters = random.sample(students, num_comments)
        
        for commenter in commenters:
            Comment.objects.get_or_create(
                user=commenter,
                post=post,
                content=random.choice(comments_templates)
            )
    
    print(f"  ✅ Total de {Comment.objects.count()} comentários criados")


def create_stories(users):
    """Criar stories ativos"""
    print("\n📖 Criando stories...")
    
    companies = [u for u in users.values() if u.user_type == 'company']
    
    stories_data = [
        {
            'title': 'Nova vaga disponível!',
            'text_content': 'Desenvolvedor Frontend Jr - Candidate-se agora!',
        },
        {
            'title': 'Workshop gratuito',
            'text_content': 'Machine Learning para iniciantes - Sábado 14h',
        },
        {
            'title': 'Conquista',
            'text_content': 'Chegamos a 10k usuários! 🎉',
        },
    ]
    
    for i, company in enumerate(companies):
        if i < len(stories_data):
            story_data = stories_data[i]
            Story.objects.create(
                user=company,
                text_content=story_data['text_content'],
                expires_at=timezone.now() + timedelta(hours=24)
            )
            print(f"  ✅ Story criado para {company.username}")


def main():
    """Função principal"""
    print("=" * 50)
    print("🚀 POPULANDO FEED DO INSTALAB")
    print("=" * 50)
    
    # Limpar dados antigos (opcional)
    # print("\n🗑️  Limpando dados antigos...")
    # Post.objects.all().delete()
    # Like.objects.all().delete()
    # Comment.objects.all().delete()
    # Follow.objects.all().delete()
    # Story.objects.all().delete()
    
    # Criar dados
    users = create_users()
    posts = create_posts(users)
    create_follows(users)
    create_likes(users, posts)
    create_comments(users, posts)
    create_stories(users)
    
    print("\n" + "=" * 50)
    print("✅ FEED POPULADO COM SUCESSO!")
    print("=" * 50)
    print(f"\n📊 Estatísticas:")
    print(f"   • {User.objects.count()} usuários")
    print(f"   • {Post.objects.count()} posts")
    print(f"   • {Like.objects.count()} likes")
    print(f"   • {Comment.objects.count()} comentários")
    print(f"   • {Follow.objects.count()} follows")
    print(f"   • {Story.objects.filter(expires_at__gt=timezone.now()).count()} stories ativos")
    
    print("\n🔐 Credenciais de teste:")
    print("   • techjr_company / teste123")
    print("   • ai_lab_usp / teste123")
    print("   • joao_dev / teste123")
    print("   • maria_data / teste123")
    print("   • pedro_mobile / teste123")
    
    print("\n🌐 Acesse: http://localhost:8000/feed/")
    print("\n" + "=" * 50)


if __name__ == '__main__':
    main()
