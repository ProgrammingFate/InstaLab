#!/usr/bin/env python3
"""
Script para gerenciamento de solicitações de projetos para empresas
Permite aceitar, rejeitar e visualizar solicitações pendentes
"""

import os
import sys
import django
from datetime import datetime

# Configurar Django
sys.path.append('/app')  # Atualizado para Docker
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.core.models import JobListing, JobApplication
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

class ProjectRequestManager:
    def __init__(self):
        self.user = None
        
    def authenticate_company(self):
        """Autentica uma empresa para usar o sistema"""
        print("🏢 Sistema de Gerenciamento de Solicitações - InstaLab")
        print("=" * 60)
        
        email = input("Digite o email da empresa: ").strip()
        
        try:
            user = User.objects.get(email=email, user_type='company')
            self.user = user
            print(f"✅ Autenticado como: {user.company_name or user.username}")
            return True
        except User.DoesNotExist:
            print("❌ Empresa não encontrada ou não é uma conta de empresa!")
            return False
    
    def list_pending_requests(self):
        """Lista todas as solicitações pendentes"""
        if not self.user:
            print("❌ Você precisa estar autenticado!")
            return
            
        # Buscar jobs da empresa
        company_jobs = JobListing.objects.filter(company=self.user)
        
        if not company_jobs.exists():
            print("📭 Sua empresa não possui vagas cadastradas.")
            return
            
        # Buscar aplicações pendentes
        pending_applications = JobApplication.objects.filter(
            job__in=company_jobs,
            status='pending'
        ).select_related('applicant', 'job')
        
        if not pending_applications.exists():
            print("✅ Não há solicitações pendentes!")
            return
            
        print(f"\n📋 Solicitações Pendentes ({pending_applications.count()}):")
        print("-" * 60)
        
        for i, application in enumerate(pending_applications, 1):
            applicant = application.applicant
            print(f"\n{i}. 👤 {applicant.nickname or applicant.username}")
            print(f"   📧 {applicant.email}")
            print(f"   🎓 {applicant.course or 'Não informado'} - {applicant.university or 'Não informado'}")
            print(f"   📝 Vaga: {application.job.title}")
            print(f"   📅 Aplicou em: {application.applied_at.strftime('%d/%m/%Y às %H:%M')}")
            if application.cover_letter:
                print(f"   💌 Carta: {application.cover_letter[:100]}...")
            print(f"   🆔 ID da Aplicação: {application.id}")
        
        return pending_applications
    
    def process_application(self, application_id, action):
        """Processa uma aplicação (aceitar ou rejeitar)"""
        try:
            application = JobApplication.objects.get(
                id=application_id,
                job__company=self.user,
                status='pending'
            )
            
            if action == 'accept':
                application.status = 'accepted'
                status_text = "✅ ACEITA"
                email_subject = f"Parabéns! Sua candidatura foi aceita - {application.job.title}"
                email_message = f"""
Olá {application.applicant.nickname or application.applicant.username}!

Temos uma ótima notícia! 🎉

Sua candidatura para a vaga "{application.job.title}" na empresa {self.user.company_name or self.user.username} foi ACEITA!

Detalhes da vaga:
- Título: {application.job.title}
- Empresa: {self.user.company_name or self.user.username}
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

Agradecemos seu interesse na vaga "{application.job.title}" na empresa {self.user.company_name or self.user.username}.

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
            
            print(f"\n{status_text}")
            print(f"👤 Candidato: {application.applicant.nickname or application.applicant.username}")
            print(f"📝 Vaga: {application.job.title}")
            print(f"{email_status}")
            
            return True
            
        except JobApplication.DoesNotExist:
            print("❌ Aplicação não encontrada ou já foi processada!")
            return False
        except Exception as e:
            print(f"❌ Erro ao processar aplicação: {str(e)}")
            return False
    
    def interactive_menu(self):
        """Menu interativo principal"""
        if not self.authenticate_company():
            return
            
        while True:
            print("\n" + "=" * 60)
            print(f"🏢 {self.user.company_name or self.user.username}")
            print("=" * 60)
            print("1. 📋 Ver solicitações pendentes")
            print("2. ✅ Aceitar solicitação")
            print("3. ❌ Rejeitar solicitação")
            print("4. 📊 Estatísticas")
            print("5. 🚪 Sair")
            print("-" * 60)
            
            choice = input("Escolha uma opção (1-5): ").strip()
            
            if choice == '1':
                self.list_pending_requests()
                
            elif choice == '2':
                pending = self.list_pending_requests()
                if pending and pending.exists():
                    try:
                        app_id = int(input("\n🆔 Digite o ID da aplicação para ACEITAR: "))
                        self.process_application(app_id, 'accept')
                    except ValueError:
                        print("❌ ID inválido!")
                        
            elif choice == '3':
                pending = self.list_pending_requests()
                if pending and pending.exists():
                    try:
                        app_id = int(input("\n🆔 Digite o ID da aplicação para REJEITAR: "))
                        self.process_application(app_id, 'reject')
                    except ValueError:
                        print("❌ ID inválido!")
                        
            elif choice == '4':
                self.show_statistics()
                
            elif choice == '5':
                print("👋 Até logo!")
                break
                
            else:
                print("❌ Opção inválida!")
    
    def show_statistics(self):
        """Mostra estatísticas da empresa"""
        if not self.user:
            return
            
        company_jobs = JobListing.objects.filter(company=self.user)
        all_applications = JobApplication.objects.filter(job__in=company_jobs)
        
        total_jobs = company_jobs.count()
        total_applications = all_applications.count()
        pending_apps = all_applications.filter(status='pending').count()
        accepted_apps = all_applications.filter(status='accepted').count()
        rejected_apps = all_applications.filter(status='rejected').count()
        
        print(f"\n📊 Estatísticas de {self.user.company_name or self.user.username}")
        print("-" * 50)
        print(f"📝 Total de vagas publicadas: {total_jobs}")
        print(f"📨 Total de candidaturas: {total_applications}")
        print(f"⏳ Pendentes: {pending_apps}")
        print(f"✅ Aceitas: {accepted_apps}")
        print(f"❌ Rejeitadas: {rejected_apps}")
        
        if total_applications > 0:
            acceptance_rate = (accepted_apps / total_applications) * 100
            print(f"📈 Taxa de aceitação: {acceptance_rate:.1f}%")

def main():
    """Função principal"""
    manager = ProjectRequestManager()
    manager.interactive_menu()

if __name__ == "__main__":
    main()
