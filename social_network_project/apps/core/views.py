from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_page
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import transaction
import logging

from .models import (
    Post, Like, Comment, Follow, Story, StoryView,
    JobListing, JobCategory, JobApplication
)
from .forms import PostForm, CommentForm, JobListingForm, JobApplicationForm

User = get_user_model()
logger = logging.getLogger(__name__)

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
    try:
        jobs = JobListing.objects.filter(status='active').select_related('company', 'category')
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
    
    except Exception as e:
        logger.error(f"Error in vagas_list: {str(e)}", exc_info=True)
        messages.error(request, 'Ocorreu um erro ao carregar as vagas. Tente novamente.')
        return render(request, 'core/vagas_list.html', {
            'page_obj': None,
            'categories': [],
            'current_category': None,
            'search_query': None,
        })

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
@transaction.atomic
def apply_job(request, job_id):
    """Candidatar-se a uma vaga"""
    try:
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
                try:
                    application = form.save(commit=False)
                    application.job = job
                    application.applicant = request.user
                    application.full_clean()  # Validate before saving
                    application.save()
                    
                    logger.info(f"User {request.user.username} applied to job {job.id}")
                    messages.success(request, 'Candidatura enviada com sucesso!')
                    return redirect('core:vaga_detail', job_id=job_id)
                except ValidationError as e:
                    messages.error(request, f'Erro de validação: {e}')
            else:
                messages.error(request, 'Por favor, corrija os erros no formulário.')
        else:
            form = JobApplicationForm()
        
        context = {
            'job': job,
            'form': form,
        }
        
        return render(request, 'core/apply_job.html', context)
    
    except Exception as e:
        logger.error(f"Error in apply_job for job {job_id}: {str(e)}", exc_info=True)
        messages.error(request, 'Ocorreu um erro ao processar sua candidatura. Tente novamente.')
        return redirect('core:vagas_list')

@login_required
@transaction.atomic
def create_job(request):
    """Criar nova vaga (apenas empresas)"""
    if not request.user.is_company():
        messages.error(request, 'Apenas empresas podem criar vagas.')
        return redirect('core:vagas_list')
    
    if request.method == 'POST':
        form = JobListingForm(request.POST)
        if form.is_valid():
            try:
                job = form.save(commit=False)
                job.company = request.user
                job.full_clean()  # Validate before saving
                job.save()
                
                logger.info(f"Company {request.user.username} created job {job.id}")
                messages.success(request, 'Vaga criada com sucesso!')
                return redirect('core:vaga_detail', job_id=job.id)
            except ValidationError as e:
                messages.error(request, f'Erro de validação: {e}')
            except Exception as e:
                logger.error(f"Error creating job: {str(e)}", exc_info=True)
                messages.error(request, 'Ocorreu um erro ao criar a vaga. Tente novamente.')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
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
    
    # Estatísticas das candidaturas
    total_count = applications.count()
    accepted_count = applications.filter(status='accepted').count()
    rejected_count = applications.filter(status='rejected').count()
    pending_count = applications.filter(status='applied').count()
    
    # Calcular porcentagens
    if total_count > 0:
        pending_percentage = round((pending_count / total_count) * 100)
        accepted_percentage = round((accepted_count / total_count) * 100)
        rejected_percentage = round((rejected_count / total_count) * 100)
        
        # Para o anel de progresso (circunferência total = 2 * π * raio)
        total_circumference = 2 * 3.14159 * 52  # raio = 52
        dash_offset = total_circumference * (1 - (total_count / max(total_count, 10)))
    else:
        pending_percentage = accepted_percentage = rejected_percentage = 0
        total_circumference = 327
        dash_offset = 327
    
    context = {
        'job': job,
        'applications': applications,
        'accepted_count': accepted_count,
        'rejected_count': rejected_count,
        'pending_count': pending_count,
        'pending_percentage': pending_percentage,
        'accepted_percentage': accepted_percentage,
        'rejected_percentage': rejected_percentage,
        'total_circumference': total_circumference,
        'dash_offset': dash_offset,
    }
    
    return render(request, 'core/job_applications.html', context)

@login_required
def instagram_feed(request):
    """Feed principal estilo Instagram"""
    try:
        # Posts dos usuários seguidos + próprios posts
        following_users = request.user.following.values_list('following', flat=True)
        
        posts = Post.objects.filter(
            Q(author__in=following_users) | Q(author=request.user),
            is_active=True
        ).select_related('author').prefetch_related('likes', 'comments')
        
        # Stories ativos
        stories = Story.objects.filter(
            user__in=following_users,
            expires_at__gt=timezone.now()
        ).select_related('user').annotate(
            view_count=Count('views')
        ).order_by('-created_at')
        
        # Adicionar informações de like para cada post
        liked_posts = Like.objects.filter(
            user=request.user,
            post__in=posts
        ).values_list('post_id', flat=True)
        
        for post in posts:
            post.user_liked = post.id in liked_posts
        
        # Paginação
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        posts_page = paginator.get_page(page_number)
        
        context = {
            'posts': posts_page,
            'stories': stories,
            'form': PostForm(),
        }
        
        return render(request, 'core/instagram_feed.html', context)
    
    except Exception as e:
        logger.error(f"Error in instagram_feed: {str(e)}", exc_info=True)
        messages.error(request, 'Ocorreu um erro ao carregar o feed. Tente novamente.')
        return render(request, 'core/instagram_feed.html', {
            'posts': [],
            'stories': [],
            'form': PostForm(),
        })


@login_required
@require_POST
@transaction.atomic
def like_post(request, post_id):
    """Toggle like em um post"""
    try:
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        
        return JsonResponse({
            'success': True,
            'liked': liked,
            'likes_count': post.likes.count()
        })
    
    except Exception as e:
        logger.error(f"Error in like_post for post {post_id}: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': 'Ocorreu um erro ao processar o like.'
        }, status=500)


@login_required
@require_POST
@transaction.atomic
def add_comment(request, post_id):
    """Adicionar comentário a um post"""
    try:
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content', '').strip()
        
        if not content:
            return JsonResponse({
                'success': False,
                'error': 'O comentário não pode estar vazio.'
            }, status=400)
        
        if len(content) > 500:
            return JsonResponse({
                'success': False,
                'error': 'O comentário não pode ter mais de 500 caracteres.'
            }, status=400)
        
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            content=content
        )
        
        logger.info(f"User {request.user.username} commented on post {post_id}")
        
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'user': comment.user.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%d/%m/%Y %H:%M')
            }
        })
    
    except Exception as e:
        logger.error(f"Error in add_comment for post {post_id}: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': 'Ocorreu um erro ao adicionar o comentário.'
        }, status=500)


@login_required
def create_post(request):
    """Criar novo post"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post criado com sucesso!')
            return redirect('core:instagram_feed')
    else:
        form = PostForm()
    
    return render(request, 'core/create_post.html', {'form': form})


@login_required
def view_story(request, story_id):
    """Visualizar story"""
    story = get_object_or_404(Story, id=story_id)
    
    # Registrar visualização
    StoryView.objects.get_or_create(story=story, user=request.user)
    
    # Buscar próximo story
    next_story = Story.objects.filter(
        user=story.user,
        created_at__gt=story.created_at,
        expires_at__gt=timezone.now()
    ).first()
    
    # Se não há próximo do mesmo usuário, buscar de outro usuário
    if not next_story:
        following_users = request.user.following.values_list('following', flat=True)
        next_story = Story.objects.filter(
            user__in=following_users,
            expires_at__gt=timezone.now()
        ).exclude(id=story.id).first()
    
    context = {
        'story': story,
        'next_story': next_story,
        'views_count': story.views.count()
    }
    
    return render(request, 'core/story_view.html', context)


@login_required
def user_profile_feed(request, username):
    """Perfil do usuário com grid de posts"""
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user, is_active=True)
    
    # Verificar se segue o usuário
    is_following = Follow.objects.filter(
        follower=request.user, 
        following=user
    ).exists() if request.user != user else False
    
    context = {
        'profile_user': user,
        'posts': posts,
        'is_following': is_following,
        'posts_count': posts.count(),
        'followers_count': user.followers.count(),
        'following_count': user.following.count(),
    }
    
    return render(request, 'core/user_profile_feed.html', context)


@login_required
@require_POST
def follow_user(request, user_id):
    """Seguir/desseguir usuário"""
    user_to_follow = get_object_or_404(User, id=user_id)
    
    if user_to_follow == request.user:
        return JsonResponse({'success': False, 'message': 'Não é possível seguir a si mesmo'})
    
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )
    
    if not created:
        follow.delete()
        following = False
        message = f'Você não segue mais {user_to_follow.username}'
    else:
        following = True
        message = f'Você agora segue {user_to_follow.username}'
    
    return JsonResponse({
        'success': True,
        'following': following,
        'message': message,
        'followers_count': user_to_follow.followers.count()
    })

# Compatibilidade com a view antiga
@login_required
def vagas(request):
    return redirect('core:vagas_list')