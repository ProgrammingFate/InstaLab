#!/usr/bin/env python3
"""
Script para popular categorias de jobs no sistema
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/lucas-dev/Desktop/instalab/InstaLab/social_network_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.core.models import JobCategory
from django.utils.text import slugify

def create_categories():
    """Criar categorias padrão para jobs"""
    categories = [
        {'name': 'Desenvolvimento Web', 'icon': '💻'},
        {'name': 'Design Gráfico', 'icon': '🎨'},
        {'name': 'Marketing Digital', 'icon': '📱'},
        {'name': 'Consultoria', 'icon': '💼'},
        {'name': 'Redação', 'icon': '✍️'},
        {'name': 'Tradução', 'icon': '🌐'},
        {'name': 'Vendas', 'icon': '📈'},
        {'name': 'Suporte Técnico', 'icon': '🔧'},
        {'name': 'Análise de Dados', 'icon': '📊'},
        {'name': 'Mobile', 'icon': '📱'},
        {'name': 'DevOps', 'icon': '⚙️'},
        {'name': 'UI/UX Design', 'icon': '🎯'},
        {'name': 'Gestão de Projetos', 'icon': '📋'},
        {'name': 'Recursos Humanos', 'icon': '👥'},
        {'name': 'Financeiro', 'icon': '💰'},
        {'name': 'Educação', 'icon': '📚'},
        {'name': 'Saúde', 'icon': '🏥'},
        {'name': 'Jurídico', 'icon': '⚖️'},
        {'name': 'Pesquisa', 'icon': '🔬'},
        {'name': 'Outros', 'icon': '🔮'},
    ]
    
    created_count = 0
    
    for cat_data in categories:
        slug = slugify(cat_data['name'])
        category, created = JobCategory.objects.get_or_create(
            slug=slug,
            defaults={
                'name': cat_data['name'],
                'icon': cat_data['icon']
            }
        )
        
        if created:
            created_count += 1
            print(f"✅ Categoria criada: {category.icon} {category.name}")
        else:
            print(f"⚠️  Categoria já existe: {category.icon} {category.name}")
    
    print(f"\n🎉 {created_count} categorias criadas!")
    print(f"📊 Total de categorias: {JobCategory.objects.count()}")

if __name__ == "__main__":
    print("🚀 Criando categorias de jobs...")
    create_categories()
    print("✅ Processo concluído!")
