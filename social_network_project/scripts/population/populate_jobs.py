#!/usr/bin/env python
import os
import sys
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('/app')  # Atualizado para Docker
django.setup()

from apps.accounts.models import CustomUser
from apps.core.models import JobCategory, JobListing

def create_categories():
    """Criar categorias de vagas"""
    categories = [
        {'name': 'Desenvolvimento', 'slug': 'desenvolvimento', 'icon': '💻'},
        {'name': 'Design', 'slug': 'design', 'icon': '🎨'},
        {'name': 'Marketing', 'slug': 'marketing', 'icon': '📊'},
        {'name': 'Pesquisa', 'slug': 'pesquisa', 'icon': '🔬'},
        {'name': 'Inovação', 'slug': 'inovacao', 'icon': '🚀'},
        {'name': 'Dados', 'slug': 'dados', 'icon': '📈'},
    ]
    
    for cat_data in categories:
        category, created = JobCategory.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        print(f"Categoria {'criada' if created else 'já existe'}: {category.name}")

def create_company_user():
    """Criar usuário empresa de exemplo"""
    if not CustomUser.objects.filter(username='techjr').exists():
        company = CustomUser.objects.create_user(
            username='techjr',
            email='contato@techjr.com',
            password='senha123',
            nickname='TechJr',
            user_type='company',
            company_name='TechJr - Empresa Júnior de Computação',
            company_description='Empresa júnior de computação focada em desenvolvimento de software e inovação tecnológica.',
            company_website='https://techjr.com'
        )
        print(f"Empresa criada: {company.company_name}")
        return company
    else:
        return CustomUser.objects.get(username='techjr')

def create_sample_jobs():
    """Criar vagas de exemplo"""
    company = create_company_user()
    
    # Obter categorias
    dev_cat = JobCategory.objects.get(slug='desenvolvimento')
    design_cat = JobCategory.objects.get(slug='design')
    research_cat = JobCategory.objects.get(slug='pesquisa')
    
    jobs = [
        {
            'title': 'Desenvolvedor Frontend React',
            'category': dev_cat,
            'description': 'Desenvolvimento de interfaces modernas com React, TypeScript e Tailwind CSS. Experiência com projetos reais para clientes.',
            'requirements': 'Conhecimento básico em React, HTML, CSS e JavaScript. Vontade de aprender e trabalhar em equipe.',
            'responsibilities': 'Desenvolver componentes React reutilizáveis, implementar designs responsivos, trabalhar com APIs REST.',
            'salary_min': Decimal('800'),
            'salary_max': Decimal('1200'),
            'spots_available': 3,
            'location': 'São Paulo, SP',
            'tags': 'React, TypeScript, Tailwind, Frontend',
            'priority': 'urgent',
        },
        {
            'title': 'Designer UX/UI',
            'category': design_cat,
            'description': 'Criação de experiências digitais inovadoras. Trabalhe com Figma, prototipagem e pesquisa de usuários em projetos reais.',
            'requirements': 'Conhecimento em Figma, noções de UX/UI, portfolio com projetos acadêmicos ou pessoais.',
            'responsibilities': 'Criar wireframes e protótipos, realizar pesquisa de usuários, desenvolver sistema de design.',
            'salary_min': Decimal('700'),
            'salary_max': Decimal('1000'),
            'spots_available': 2,
            'location': 'São Paulo, SP',
            'remote_work': True,
            'tags': 'Figma, UX Research, Prototipagem, Design System',
            'priority': 'featured',
        },
        {
            'title': 'Pesquisador IA & Machine Learning',
            'category': research_cat,
            'description': 'Desenvolvimento de algoritmos de ML e análise de dados. Oportunidade única de trabalhar com pesquisa de ponta em IA.',
            'requirements': 'Conhecimento em Python, interesse em Machine Learning, cursando Ciência da Computação ou área relacionada.',
            'responsibilities': 'Implementar algoritmos de ML, analisar datasets, documentar pesquisas, apresentar resultados.',
            'salary_min': Decimal('1000'),
            'salary_max': Decimal('1500'),
            'spots_available': 1,
            'location': 'Remoto',
            'remote_work': True,
            'tags': 'Python, TensorFlow, Data Science, Machine Learning',
            'priority': 'featured',
        }
    ]
    
    for job_data in jobs:
        job, created = JobListing.objects.get_or_create(
            title=job_data['title'],
            company=company,
            defaults=job_data
        )
        print(f"Vaga {'criada' if created else 'já existe'}: {job.title}")

if __name__ == '__main__':
    print("Populando banco de dados com categorias e vagas...")
    create_categories()
    create_sample_jobs()
    print("Concluído!")
