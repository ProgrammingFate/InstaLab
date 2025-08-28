from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.core.models import JobListing, JobApplication, JobCategory
from django.core.mail import send_mail
from django.conf import settings
import sys

User = get_user_model()

class Command(BaseCommand):
    help = 'Gerenciamento de solicitações de projetos para empresas'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email da empresa')
        parser.add_argument('--action', choices=['list', 'accept', 'reject'], help='Ação a ser executada')
        parser.add_argument('--application-id', type=int, help='ID da aplicação para aceitar/rejeitar')

    def handle(self, *args, **options):
        if options['email']:
            try:
                user = User.objects.get(email=options['email'], user_type='company')
                
                if options['action'] == 'list':
                    self.list_applications(user)
                elif options['action'] in ['accept', 'reject'] and options['application_id']:
                    self.process_application(user, options['application_id'], options['action'])
                else:
                    self.interactive_mode(user)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR('❌ Empresa não encontrada ou não é uma conta de empresa!')
                )
        else:
            self.interactive_login()

    def interactive_login(self):
        """Modo interativo para login"""
        self.stdout.write(self.style.SUCCESS('🏢 Sistema de Gerenciamento de Solicitações - InstaLab'))
        self.stdout.write('=' * 60)
        
        email = input('Digite o email da empresa: ').strip()
        
        try:
            user = User.objects.get(email=email, user_type='company')
            self.stdout.write(
                self.style.SUCCESS(f'✅ Autenticado como: {user.company_name or user.username}')
            )
            self.interactive_mode(user)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('❌ Empresa não encontrada ou não é uma conta de empresa!')
            )

    def interactive_mode(self, user):
        """Modo interativo principal"""
        while True:
            self.stdout.write('\n' + '=' * 60)
            self.stdout.write(self.style.SUCCESS(f'🏢 {user.company_name or user.username}'))
            self.stdout.write('=' * 60)
            self.stdout.write('1. 📋 Ver solicitações pendentes')
            self.stdout.write('2. ✅ Aceitar solicitação')
            self.stdout.write('3. ❌ Rejeitar solicitação')
            self.stdout.write('4. 📊 Estatísticas')
            self.stdout.write('5. 🚪 Sair')
            self.stdout.write('-' * 60)
            
            choice = input('Escolha uma opção (1-5): ').strip()
            
            if choice == '1':
                self.list_applications(user)
            elif choice == '2':
                pending = self.list_applications(user, return_data=True)
                if pending and pending.exists():
                    try:
                        app_id = int(input('\n🆔 Digite o ID da aplicação para ACEITAR: '))
                        self.process_application(user, app_id, 'accept')
                    except ValueError:
                        self.stdout.write(self.style.ERROR('❌ ID inválido!'))
            elif choice == '3':
                pending = self.list_applications(user, return_data=True)
                if pending and pending.exists():
                    try:
                        app_id = int(input('\n🆔 Digite o ID da aplicação para REJEITAR: '))
                        self.process_application(user, app_id, 'reject')
                    except ValueError:
                        self.stdout.write(self.style.ERROR('❌ ID inválido!'))
            elif choice == '4':
                self.show_statistics(user)
            elif choice == '5':
                self.stdout.write(self.style.SUCCESS('👋 Até logo!'))
                break
            else:
                self.stdout.write(self.style.ERROR('❌ Opção inválida!'))

    def list_applications(self, user, return_data=False):
        """Lista aplicações pendentes"""
        company_jobs = JobListing.objects.filter(company=user)
        
        if not company_jobs.exists():
            self.stdout.write(self.style.WARNING('📭 Sua empresa não possui vagas cadastradas.'))
            return None
            
        pending_applications = JobApplication.objects.filter(
            job__in=company_jobs,
            status='applied'
        ).select_related('applicant', 'job')
        
        if not pending_applications.exists():
            self.stdout.write(self.style.SUCCESS('✅ Não há solicitações pendentes!'))
            return None
            
        self.stdout.write(f'\n📋 Solicitações Pendentes ({pending_applications.count()}):')
        self.stdout.write('-' * 60)
        
        for i, application in enumerate(pending_applications, 1):
            applicant = application.applicant
            self.stdout.write(f'\n{i}. 👤 {applicant.nickname or applicant.username}')
            self.stdout.write(f'   📧 {applicant.email}')
            if applicant.course:
                self.stdout.write(f'   🎓 {applicant.course} - {applicant.university or "Não informado"}')
            self.stdout.write(f'   📝 Vaga: {application.job.title}')
            self.stdout.write(f'   📅 Aplicou em: {application.applied_at.strftime("%d/%m/%Y às %H:%M")}')
            if application.cover_letter:
                preview = application.cover_letter[:100] + '...' if len(application.cover_letter) > 100 else application.cover_letter
                self.stdout.write(f'   💌 Carta: {preview}')
            self.stdout.write(f'   🆔 ID da Aplicação: {application.id}')
        
        return pending_applications if return_data else None

    def process_application(self, user, application_id, action):
        """Processa uma aplicação"""
        try:
            application = JobApplication.objects.get(
                id=application_id,
                job__company=user,
                status='applied'
            )
            
            if action == 'accept':
                application.status = 'accepted'
                status_text = "✅ ACEITA"
                email_subject = f"Parabéns! Sua candidatura foi aceita - {application.job.title}"
                email_message = f"""
Olá {application.applicant.nickname or application.applicant.username}!

Temos uma ótima notícia! 🎉

Sua candidatura para a vaga "{application.job.title}" na empresa {user.company_name or user.username} foi ACEITA!

Detalhes da vaga:
- Título: {application.job.title}
- Empresa: {user.company_name or user.username}
- Data da candidatura: {application.applied_at.strftime('%d/%m/%Y')}

Nossa equipe entrará em contato em breve para os próximos passos.

Atenciosamente,
Equipe InstaLab
                """
            else:  # reject
                application.status = 'rejected'
                status_text = "❌ REJEITADA"
                email_subject = f"Atualização sobre sua candidatura - {application.job.title}"
                email_message = f"""
Olá {application.applicant.nickname or application.applicant.username},

Agradecemos seu interesse na vaga "{application.job.title}" na empresa {user.company_name or user.username}.

Após análise cuidadosa, decidimos seguir com outros candidatos para esta posição.

Não desanime! Continue se candidatando a outras oportunidades em nossa plataforma.

Atenciosamente,
Equipe InstaLab
                """
            
            application.save()
            
            # Enviar email (se configurado)
            try:
                send_mail(
                    email_subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [application.applicant.email],
                    fail_silently=True,
                )
                email_status = "📧 Email enviado"
            except Exception as e:
                email_status = f"⚠️ Erro ao enviar email: {str(e)}"
            
            self.stdout.write(f'\n{status_text}')
            self.stdout.write(f'👤 Candidato: {application.applicant.nickname or application.applicant.username}')
            self.stdout.write(f'📝 Vaga: {application.job.title}')
            self.stdout.write(self.style.SUCCESS(email_status))
            
        except JobApplication.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ Aplicação não encontrada ou já foi processada!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro ao processar aplicação: {str(e)}'))

    def show_statistics(self, user):
        """Mostra estatísticas da empresa"""
        company_jobs = JobListing.objects.filter(company=user)
        all_applications = JobApplication.objects.filter(job__in=company_jobs)
        
        total_jobs = company_jobs.count()
        total_applications = all_applications.count()
        pending_apps = all_applications.filter(status='applied').count()
        accepted_apps = all_applications.filter(status='accepted').count()
        rejected_apps = all_applications.filter(status='rejected').count()
        
        self.stdout.write(f'\n📊 Estatísticas de {user.company_name or user.username}')
        self.stdout.write('-' * 50)
        self.stdout.write(f'📝 Total de vagas publicadas: {total_jobs}')
        self.stdout.write(f'📨 Total de candidaturas: {total_applications}')
        self.stdout.write(f'⏳ Pendentes: {pending_apps}')
        self.stdout.write(f'✅ Aceitas: {accepted_apps}')
        self.stdout.write(f'❌ Rejeitadas: {rejected_apps}')
        
        if total_applications > 0:
            acceptance_rate = (accepted_apps / total_applications) * 100
            self.stdout.write(f'📈 Taxa de aceitação: {acceptance_rate:.1f}%')
