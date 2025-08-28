#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('/app')  # Atualizado para Docker
django.setup()

from apps.accounts.models import CustomUser

def create_test_users():
    """Criar usuários de teste"""
    
    # Criar estudante
    if not CustomUser.objects.filter(username='joao_estudante').exists():
        student = CustomUser.objects.create_user(
            username='joao_estudante',
            email='joao@email.com',
            password='senha123',
            nickname='JoãoEst',
            user_type='student',
            course='Ciência da Computação',
            university='USP',
            semester='5º semestre'
        )
        print(f"Estudante criado: {student.nickname}")
    else:
        print("Estudante já existe")
    
    # Verificar se a empresa já existe
    if CustomUser.objects.filter(username='techjr').exists():
        print("Empresa TechJr já existe")
    else:
        print("Empresa TechJr não encontrada")

if __name__ == '__main__':
    print("Criando usuários de teste...")
    create_test_users()
    print("Concluído!")
