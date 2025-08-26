from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import Post, JobListing, JobCategory, JobApplication
from .forms import JobListingForm, JobApplicationForm

def home(request):
    posts = Post.objects.all()  # Fetch all posts
    return render(request, 'core/home.html', {'posts': posts})

@login_required
def search(request):
    query = request.GET.get('q')
    if query:
        results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    else:
        results = Post.objects.none()
    return render(request, 'core/search.html', {'results': results, 'query': query})

@login_required
def vagas_list(request):
    """Lista todas as vagas com filtros"""
    jobs = JobListing.objects.filter(status='active')
    categories = JobCategory.objects.all()
    
    # Filtros
    category_filter = request.GET.get('category')
    search_query = request.GET.get('q')
    
    if category_filter:
        jobs = jobs.filter(category__slug=category_filter)
    
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(company__company_name__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Paginação
    paginator = Paginator(jobs, 6)  # 6 vagas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_filter,
        'search_query': search_query,
    }
    
    return render(request, 'core/vagas_list.html', context)

@login_required
def vaga_detail(request, job_id):
    """Detalhes de uma vaga específica"""
    job = get_object_or_404(JobListing, id=job_id, status='active')
    user_application = None
    
    # Verificar se o usuário já se candidatou
    if request.user.is_authenticated:
        try:
            user_application = JobApplication.objects.get(job=job, applicant=request.user)
        except JobApplication.DoesNotExist:
            pass
    
    context = {
        'job': job,
        'user_application': user_application,
        'can_apply': request.user.is_student() and not user_application and not job.is_deadline_passed(),
    }
    
    return render(request, 'core/vaga_detail.html', context)

@login_required
def apply_job(request, job_id):
    """Candidatar-se a uma vaga"""
    job = get_object_or_404(JobListing, id=job_id, status='active')
    
    # Verificações
    if not request.user.is_student():
        messages.error(request, 'Apenas estudantes podem se candidatar às vagas.')
        return redirect('core:vaga_detail', job_id=job_id)
    
    if job.is_deadline_passed():
        messages.error(request, 'O prazo para esta vaga já expirou.')
        return redirect('core:vaga_detail', job_id=job_id)
    
    # Verificar se já se candidatou
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'Você já se candidatou para esta vaga.')
        return redirect('core:vaga_detail', job_id=job_id)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            
            messages.success(request, 'Candidatura enviada com sucesso!')
            return redirect('core:vaga_detail', job_id=job_id)
    else:
        form = JobApplicationForm()
    
    context = {
        'job': job,
        'form': form,
    }
    
    return render(request, 'core/apply_job.html', context)

@login_required
def create_job(request):
    """Criar nova vaga (apenas empresas)"""
    if not request.user.is_company():
        messages.error(request, 'Apenas empresas podem criar vagas.')
        return redirect('core:vagas_list')
    
    if request.method == 'POST':
        form = JobListingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user
            job.save()
            
            messages.success(request, 'Vaga criada com sucesso!')
            return redirect('core:vaga_detail', job_id=job.id)
    else:
        form = JobListingForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'core/create_job.html', context)

@login_required
def my_applications(request):
    """Minhas candidaturas (para estudantes)"""
    if not request.user.is_student():
        messages.error(request, 'Acesso restrito para estudantes.')
        return redirect('core:vagas_list')
    
    applications = JobApplication.objects.filter(applicant=request.user).order_by('-applied_at')
    
    context = {
        'applications': applications,
    }
    
    return render(request, 'core/my_applications.html', context)

@login_required
def my_jobs(request):
    """Minhas vagas (para empresas)"""
    if not request.user.is_company():
        messages.error(request, 'Acesso restrito para empresas.')
        return redirect('core:vagas_list')
    
    jobs = JobListing.objects.filter(company=request.user).order_by('-created_at')
    
    context = {
        'jobs': jobs,
    }
    
    return render(request, 'core/my_jobs.html', context)

@login_required
def job_applications(request, job_id):
    """Ver candidaturas de uma vaga (apenas para o criador da vaga)"""
    job = get_object_or_404(JobListing, id=job_id, company=request.user)
    applications = JobApplication.objects.filter(job=job).order_by('-applied_at')
    
    context = {
        'job': job,
        'applications': applications,
    }
    
    return render(request, 'core/job_applications.html', context)

# Compatibilidade com a view antiga
@login_required
def vagas(request):
    return redirect('core:vagas_list')