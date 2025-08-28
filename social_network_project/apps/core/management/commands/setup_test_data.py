from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.core.models import JobListing, JobApplication, JobCategory
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Cria vagas e candidaturas de teste'

    def handle(self, *args, **options):
        # Criar empresa de teste se não existir
        company_email = "empresa@test.com"
        company, created = User.objects.get_or_create(
            email=company_email,
            defaults={
                'username': 'empresatest',
                'nickname': 'TechJr',
                'user_type': 'company',
                'company_name': 'TechJr - Empresa Júnior',
                'company_description': 'Empresa Júnior focada em tecnologia e inovação'
            }
        )
        
        if created:
            company.set_password('123456')
            company.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Empresa criada: {company.company_name}'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️ Empresa já existe: {company.company_name}'))

        # Criar estudante de teste se não existir
        student_email = "estudante@test.com"
        try:
            student = User.objects.get(email=student_email)
            self.stdout.write(self.style.WARNING(f'⚠️ Estudante já existe: {student.nickname}'))
        except User.DoesNotExist:
            student = User.objects.create_user(
                username='estudantetest',
                email=student_email,
                password='123456',
                nickname='JoãoTestador',
                user_type='student',
                course='Ciência da Computação',
                university='UFMG',
                semester='6º período'
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Estudante criado: {student.nickname}'))

        # Criar categorias se não existirem
        dev_category, _ = JobCategory.objects.get_or_create(
            slug='desenvolvimento-web',
            defaults={'name': 'Desenvolvimento Web', 'icon': '💻'}
        )
        
        design_category, _ = JobCategory.objects.get_or_create(
            slug='design-grafico',
            defaults={'name': 'Design Gráfico', 'icon': '🎨'}
        )

        # Criar vagas de teste
        jobs_data = [
            {
                'title': 'Desenvolvedor Frontend React',
                'category': dev_category,
                'description': 'Procuramos um desenvolvedor frontend para trabalhar com React e TypeScript em projetos inovadores.',
                'requirements': 'Conhecimento em React, TypeScript, HTML, CSS',
                'responsibilities': 'Desenvolver interfaces responsivas, colaborar com o time de design',
                'salary_min': 800.00,
                'salary_max': 1200.00,
                'location': 'Belo Horizonte, MG',
                'tags': 'React, TypeScript, Frontend, JavaScript',
                'deadline': timezone.now() + timedelta(days=30)
            },
            {
                'title': 'Designer UI/UX',
                'category': design_category,
                'description': 'Buscamos um designer criativo para criar experiências incríveis para nossos usuários.',
                'requirements': 'Figma, Adobe XD, conhecimento em UX',
                'responsibilities': 'Criar protótipos, pesquisa com usuários, design de interfaces',
                'location': 'Remoto',
                'tags': 'UI, UX, Figma, Design',
                'deadline': timezone.now() + timedelta(days=45),
                'remote_work': True
            },
            {
                'title': 'Estagiário de Marketing Digital',
                'category': JobCategory.objects.get(slug='marketing-digital'),
                'description': 'Oportunidade para aprender marketing digital trabalhando em campanhas reais.',
                'requirements': 'Interesse em marketing, redes sociais',
                'responsibilities': 'Criação de conteúdo, análise de métricas, gestão de redes sociais',
                'location': 'Híbrido - BH',
                'tags': 'Marketing, Redes Sociais, Analytics',
                'deadline': timezone.now() + timedelta(days=20)
            }
        ]

        created_jobs = []
        for job_data in jobs_data:
            job, created = JobListing.objects.get_or_create(
                title=job_data['title'],
                company=company,
                defaults=job_data
            )
            
            if created:
                created_jobs.append(job)
                self.stdout.write(self.style.SUCCESS(f'✅ Vaga criada: {job.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️ Vaga já existe: {job.title}'))

        # Criar candidaturas de teste
        if created_jobs:
            for job in created_jobs[:2]:  # Candidatar apenas às 2 primeiras vagas
                application, created = JobApplication.objects.get_or_create(
                    job=job,
                    applicant=student,
                    defaults={
                        'cover_letter': f'Olá! Tenho muito interesse na vaga de {job.title}. Sou estudante de {student.course} e acredito que posso contribuir muito com o projeto. Tenho experiência em projetos acadêmicos e estou sempre buscando aprender mais.',
                        'status': 'applied'
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'✅ Candidatura criada: {student.nickname} -> {job.title}'))
                else:
                    self.stdout.write(self.style.WARNING(f'⚠️ Candidatura já existe: {student.nickname} -> {job.title}'))

        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('🎉 Setup de teste concluído!'))
        self.stdout.write('\n📝 Para testar o sistema de gerenciamento de candidaturas:')
        self.stdout.write(f'   Email da empresa: {company_email}')
        self.stdout.write(f'   Senha: 123456')
        self.stdout.write('\n💡 Execute o comando:')
        self.stdout.write('   python manage.py manage_applications --email empresa@test.com')
        self.stdout.write('=' * 60)
