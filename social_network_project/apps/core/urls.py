from django.urls import path
from . import views

app_name = "core"  

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    
    # Vagas URLs
    path('vagas/', views.vagas_list, name='vagas_list'),
    path('vagas/criar/', views.create_job, name='create_job'),
    path('vagas/<int:job_id>/', views.vaga_detail, name='vaga_detail'),
    path('vagas/<int:job_id>/candidatar/', views.apply_job, name='apply_job'),
    path('vagas/<int:job_id>/candidaturas/', views.job_applications, name='job_applications'),
    
    # Minhas páginas
    path('minhas-candidaturas/', views.my_applications, name='my_applications'),
    path('minhas-vagas/', views.my_jobs, name='my_jobs'),
    
    # Compatibilidade
    path('vagas-old/', views.vagas, name='vagas'),
]