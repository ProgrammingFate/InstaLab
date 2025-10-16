"""
Script para popular o feed do Instagram com posts de exemplo
"""
import os
import sys
import django

# Configurar Django
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.core.models import Post, Like, Comment, Follow, Story
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()

def create_sample_posts():
    """Criar posts de exemplo"""
    print("🎨 Criando posts de exemplo...")
    
    # Buscar todos os usuários
    users = list(User.objects.all())
    if len(users) < 2:
        print("❌ Precisa de pelo menos 2 usuários cadastrados!")
        print("💡 Crie usuários primeiro usando create_test_users.py")
        return
    
    # Conteúdos de exemplo
    sample_contents = [
        "Acabei de lançar meu novo projeto! 🚀 #coding #developer",
        "Aprendendo muito sobre Machine Learning hoje! 🤖 #AI #ML",
        "Que vista incrível do nosso laboratório! 🔬 #ciencia #pesquisa",
        "Equipe trabalhando forte no novo produto! 💪 #teamwork",
        "Palestra incrível sobre inovação tecnológica! 🎤 #tech #innovation",
        "Networking é tudo! Ótimo encontro hoje 🤝 #networking #business",
        "Feliz com os resultados do semestre! 📊 #success #growth",
        "Café e código, a combinação perfeita! ☕💻 #devlife",
        "Workshop de Python foi demais! 🐍 #python #programming",
        "Finalmente terminei esse projeto! 🎉 #achievement",
        "Estudando para as provas finais 📚 #estudante #universidade",
        "Nova vaga disponível na nossa empresa! 💼 #jobs #oportunidade",
        "Robótica é o futuro! 🤖 #robotics #engineering",
        "Apresentação do TCC hoje, desejem sorte! 🍀 #tcc #faculdade",
        "Hackathon foi incrível, time arrasou! 🏆 #hackathon #winners",
    ]
    
    # Criar posts para cada usuário
    posts_created = 0
    for user in users:
        # Cada usuário cria de 2 a 5 posts
        num_posts = random.randint(2, 5)
        
        for i in range(num_posts):
            content = random.choice(sample_contents)
            
            # Criar post com data aleatória nos últimos 7 dias
            days_ago = random.randint(0, 7)
            hours_ago = random.randint(0, 23)
            
            post = Post.objects.create(
                author=user,
                content=content,
                post_type=random.choice(['photo', 'text', 'project']),
                is_active=True
            )
            
            # Ajustar a data de criação
            post.created_at = timezone.now() - timedelta(days=days_ago, hours=hours_ago)
            post.save()
            
            posts_created += 1
    
    print(f"✅ {posts_created} posts criados!")
    return Post.objects.all()


def create_sample_likes(posts):
    """Criar likes de exemplo"""
    print("❤️ Adicionando likes aos posts...")
    
    users = list(User.objects.all())
    likes_created = 0
    
    for post in posts:
        # Cada post recebe de 1 a 10 likes de usuários aleatórios
        num_likes = random.randint(1, min(10, len(users)))
        likers = random.sample(users, num_likes)
        
        for user in likers:
            # Não deixar o autor dar like no próprio post
            if user != post.author:
                Like.objects.get_or_create(
                    user=user,
                    post=post
                )
                likes_created += 1
    
    print(f"✅ {likes_created} likes adicionados!")


def create_sample_comments(posts):
    """Criar comentários de exemplo"""
    print("💬 Adicionando comentários aos posts...")
    
    users = list(User.objects.all())
    
    sample_comments = [
        "Muito legal! 🔥",
        "Parabéns pelo trabalho! 👏",
        "Incrível! Quando vai lançar?",
        "Show de bola! 🎉",
        "Adorei! Continue assim 💪",
        "Top demais! 🚀",
        "Que legal, vou conferir!",
        "Ficou show! Parabéns 🎊",
        "Excelente conteúdo! 📚",
        "Inspirador! 💡",
        "Sensacional! 🌟",
        "Mandou bem! 👍",
        "Muito bom, quero participar!",
        "Sucesso! 🍀",
        "Que demais! 😍",
    ]
    
    comments_created = 0
    
    for post in posts:
        # Cada post recebe de 0 a 5 comentários
        num_comments = random.randint(0, 5)
        
        for _ in range(num_comments):
            user = random.choice(users)
            content = random.choice(sample_comments)
            
            Comment.objects.create(
                user=user,
                post=post,
                content=content
            )
            comments_created += 1
    
    print(f"✅ {comments_created} comentários adicionados!")


def create_sample_follows():
    """Criar relações de seguir entre usuários"""
    print("👥 Criando relações de seguir...")
    
    users = list(User.objects.all())
    follows_created = 0
    
    for user in users:
        # Cada usuário segue de 1 a 5 outros usuários
        num_follows = random.randint(1, min(5, len(users) - 1))
        
        # Escolher usuários aleatórios para seguir (exceto ele mesmo)
        potential_follows = [u for u in users if u != user]
        to_follow = random.sample(potential_follows, num_follows)
        
        for followed_user in to_follow:
            Follow.objects.get_or_create(
                follower=user,
                following=followed_user
            )
            follows_created += 1
    
    print(f"✅ {follows_created} relações de seguir criadas!")


def create_sample_stories():
    """Criar stories de exemplo"""
    print("📸 Criando stories...")
    
    users = list(User.objects.all())
    
    story_texts = [
        "Bom dia! ☀️",
        "Trabalhando duro! 💻",
        "Almoço merecido! 🍔",
        "Reunião importante! 📊",
        "Sexta-feira! 🎉",
        "Fim de semana chegando! 😎",
        "Estudando muito! 📚",
        "Código funcionando! ✅",
        "Deploy realizado! 🚀",
        "Time unido! 👊",
    ]
    
    stories_created = 0
    
    # Alguns usuários aleatórios criam stories
    story_users = random.sample(users, min(5, len(users)))
    
    for user in story_users:
        # Cada usuário cria de 1 a 3 stories
        num_stories = random.randint(1, 3)
        
        for _ in range(num_stories):
            text = random.choice(story_texts)
            
            story = Story.objects.create(
                user=user,
                text_content=text,
                background_color=random.choice(['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']),
                text_color='#FFFFFF',
                expires_at=timezone.now() + timedelta(hours=24)
            )
            stories_created += 1
    
    print(f"✅ {stories_created} stories criados!")


def main():
    """Função principal"""
    print("=" * 50)
    print("🎨 POPULANDO FEED DO INSTAGRAM")
    print("=" * 50)
    
    # Criar posts
    posts = create_sample_posts()
    
    if posts and posts.count() > 0:
        # Criar interações
        create_sample_likes(posts)
        create_sample_comments(posts)
        create_sample_follows()
        create_sample_stories()
        
        print("\n" + "=" * 50)
        print("✅ FEED POPULADO COM SUCESSO!")
        print("=" * 50)
        print(f"\n📊 Resumo:")
        print(f"   Posts: {Post.objects.count()}")
        print(f"   Likes: {Like.objects.count()}")
        print(f"   Comentários: {Comment.objects.count()}")
        print(f"   Seguidores: {Follow.objects.count()}")
        print(f"   Stories: {Story.objects.filter(expires_at__gt=timezone.now()).count()}")
        print(f"\n🌐 Acesse: http://127.0.0.1:8000/feed/")
    else:
        print("\n❌ Nenhum post criado. Verifique se há usuários cadastrados.")


if __name__ == '__main__':
    main()
