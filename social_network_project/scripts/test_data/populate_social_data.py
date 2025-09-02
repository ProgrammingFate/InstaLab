#!/usr/bin/env python3
"""
Script para popular dados de teste para o sistema de Stories e Área Social
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Configurar Django
sys.path.append('/app')  # Para Docker
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.messaging.models import Story, StudentPost, StudyGroup
from apps.core.models import JobListing, JobCategory

User = get_user_model()

def create_test_stories():
    """Criar stories de exemplo para empresas"""
    print("🎬 Criando stories de exemplo...")
    
    # Buscar empresa de teste
    try:
        company = User.objects.get(email='empresa@test.com')
    except User.DoesNotExist:
        print("❌ Empresa de teste não encontrada. Execute o setup_test_data primeiro.")
        return
    
    # Buscar uma vaga para relacionar
    job = JobListing.objects.filter(company=company).first()
    
    stories_data = [
        {
            'title': '🚀 Nova Vaga Disponível!',
            'content': 'Estamos com uma nova oportunidade incrível para desenvolvedores React! Venha fazer parte do nosso time e desenvolver projetos inovadores.',
            'story_type': 'job',
            'related_job': job,
            'is_highlighted': True,
        },
        {
            'title': '🏆 Projeto Entregue com Sucesso!',
            'content': 'Acabamos de entregar mais um projeto incrível para nosso cliente! Sistema completo de gestão desenvolvido em Django + React.',
            'story_type': 'achievement',
            'is_highlighted': False,
        },
        {
            'title': '📚 Workshop de Python',
            'content': 'Na próxima sexta teremos um workshop gratuito de Python para iniciantes! Inscrições abertas no nosso site.',
            'story_type': 'event',
            'external_link': 'https://example.com/workshop',
            'is_highlighted': False,
        },
        {
            'title': '💼 Cultura da Empresa',
            'content': 'Conheça mais sobre nossa cultura de inovação e aprendizado contínuo. Aqui cada membro é valorizado e incentivado a crescer!',
            'story_type': 'culture',
            'is_highlighted': False,
        }
    ]
    
    created_count = 0
    for story_data in stories_data:
        story, created = Story.objects.get_or_create(
            user=company,
            title=story_data['title'],
            defaults=story_data
        )
        if created:
            created_count += 1
            print(f"✅ Story criado: {story.title}")
        else:
            print(f"⚠️ Story já existe: {story.title}")
    
    print(f"🎉 {created_count} stories criados!")

def create_test_student_posts():
    """Criar posts de exemplo para estudantes"""
    print("📝 Criando posts de estudantes...")
    
    # Buscar estudante de teste
    try:
        student = User.objects.get(email='estudante@test.com')
    except User.DoesNotExist:
        print("❌ Estudante de teste não encontrado. Execute o setup_test_data primeiro.")
        return
    
    posts_data = [
        {
            'title': '💡 Alguém pode me ajudar com React Hooks?',
            'content': 'Estou aprendendo React e estou com dificuldades para entender como usar useEffect corretamente. Alguém tem alguma dica ou material bom para indicar?',
            'post_type': 'help',
            'tags': 'react, javascript, hooks, frontend',
        },
        {
            'title': '🚀 Acabei de terminar meu primeiro projeto em Django!',
            'content': 'Pessoal, consegui finalizar meu primeiro projeto completo em Django! É um sistema de biblioteca simples, mas estou muito orgulhoso do resultado. Foi desafiador mas aprendi muito!',
            'post_type': 'achievement',
            'tags': 'django, python, projeto, backend',
        },
        {
            'title': '📚 Grupo de Estudos - Algoritmos e Estruturas de Dados',
            'content': 'Estou organizando um grupo de estudos para a matéria de Algoritmos e Estruturas de Dados. Vamos nos reunir duas vezes por semana online para resolver exercícios juntos!',
            'post_type': 'study_group',
            'study_subject': 'Algoritmos e Estruturas de Dados',
            'max_participants': 8,
            'tags': 'algoritmos, estruturas-dados, grupo-estudos',
        },
        {
            'title': '🤝 Procuro parceiro para hackathon',
            'content': 'Alguém está interessado em formar dupla para o hackathon da universidade? Tenho experiência com Python e estou aprendendo React. Seria legal ter alguém com mais experiência em frontend!',
            'post_type': 'networking',
            'tags': 'hackathon, python, react, networking',
        },
        {
            'title': '💭 O que vocês acham sobre aprender IA/ML?',
            'content': 'Estou pensando em começar a estudar Machine Learning e IA. Para quem já estuda ou trabalha na área, qual a melhor forma de começar? Python é realmente essencial?',
            'post_type': 'discussion',
            'tags': 'machine-learning, ia, python, carreira',
        }
    ]
    
    created_count = 0
    for post_data in posts_data:
        post, created = StudentPost.objects.get_or_create(
            author=student,
            title=post_data['title'],
            defaults=post_data
        )
        if created:
            created_count += 1
            print(f"✅ Post criado: {post.title}")
        else:
            print(f"⚠️ Post já existe: {post.title}")
    
    print(f"🎉 {created_count} posts criados!")

def create_test_study_groups():
    """Criar grupos de estudo de exemplo"""
    print("👥 Criando grupos de estudo...")
    
    # Buscar estudante de teste
    try:
        student = User.objects.get(email='estudante@test.com')
    except User.DoesNotExist:
        print("❌ Estudante de teste não encontrado.")
        return
    
    groups_data = [
        {
            'name': 'Python para Iniciantes',
            'description': 'Grupo para quem está começando a aprender Python. Vamos estudar desde o básico até conceitos mais avançados, sempre com muito código prático!',
            'subject': 'Python',
            'max_members': 12,
            'meeting_type': 'online',
            'university': 'USP',
            'semester': '2024.2',
        },
        {
            'name': 'Cálculo I - Revisão para P2',
            'description': 'Grupo focado em revisar os conteúdos de Cálculo I para a segunda prova. Vamos resolver exercícios e tirar dúvidas juntos.',
            'subject': 'Cálculo I',
            'max_members': 8,
            'meeting_type': 'presential',
            'university': 'USP',
            'semester': '2024.2',
        },
        {
            'name': 'Web Development Full Stack',
            'description': 'Grupo para estudar desenvolvimento web completo: HTML, CSS, JavaScript, React, Node.js, bancos de dados e deploy.',
            'subject': 'Desenvolvimento Web',
            'max_members': 15,
            'meeting_type': 'hybrid',
        },
        {
            'name': 'Preparação para Entrevistas Tech',
            'description': 'Grupo focado em preparação para entrevistas técnicas em empresas de tecnologia. Vamos praticar algoritmos, estruturas de dados e soft skills.',
            'subject': 'Preparação para Entrevistas',
            'max_members': 10,
            'meeting_type': 'online',
        }
    ]
    
    created_count = 0
    for group_data in groups_data:
        group, created = StudyGroup.objects.get_or_create(
            creator=student,
            name=group_data['name'],
            defaults=group_data
        )
        if created:
            group.members.add(student)  # Criador automaticamente vira membro
            created_count += 1
            print(f"✅ Grupo criado: {group.name}")
        else:
            print(f"⚠️ Grupo já existe: {group.name}")
    
    print(f"🎉 {created_count} grupos de estudo criados!")

def main():
    """Função principal"""
    print("🚀 Populando dados de teste para Stories e Área Social...")
    print("=" * 60)
    
    create_test_stories()
    print()
    create_test_student_posts()
    print()
    create_test_study_groups()
    
    print()
    print("✅ Processo concluído!")
    print("📊 Resumo:")
    print(f"   - Stories: {Story.objects.count()}")
    print(f"   - Posts de Estudantes: {StudentPost.objects.count()}")
    print(f"   - Grupos de Estudo: {StudyGroup.objects.count()}")

if __name__ == "__main__":
    main()
