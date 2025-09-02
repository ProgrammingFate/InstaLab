from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Q, Max, Count
from django.contrib import messages
from django.core.paginator import Paginator
from .models import (
    Conversation, ChatMessage, Story, StoryView,
    StudentPost, PostLike, PostComment, StudentConnection, StudyGroup
)
from .forms import StoryForm, ChatMessageForm, StudentPostForm, StudyGroupForm

User = get_user_model()

@login_required
def conversations_list(request):
    """Lista todas as conversas do usuário"""
    conversations = Conversation.objects.filter(
        participants=request.user
    ).annotate(
        last_message_time=Max('messages__timestamp')
    ).order_by('-last_message_time')
    
    return render(request, 'messaging/conversations_list.html', {
        'conversations': conversations
    })

@login_required
def chat_view(request, conversation_id=None):
    """View principal do chat"""
    if conversation_id:
        conversation = get_object_or_404(
            Conversation, 
            id=conversation_id, 
            participants=request.user
        )
    else:
        # Criar nova conversa ou redirecionar
        other_user_id = request.GET.get('user_id')
        if other_user_id:
            other_user = get_object_or_404(User, id=other_user_id)
            # Verificar se já existe conversa entre os dois usuários
            conversation = Conversation.objects.filter(
                participants=request.user
            ).filter(
                participants=other_user
            ).first()
            
            if not conversation:
                # Criar nova conversa
                conversation = Conversation.objects.create()
                conversation.participants.add(request.user, other_user)
        else:
            return redirect('messaging:conversations_list')
    
    # Marcar mensagens como lidas
    ChatMessage.objects.filter(
        conversation=conversation,
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)
    
    # Buscar mensagens
    chat_messages = conversation.messages.all()
    other_user = conversation.participants.exclude(id=request.user.id).first()
    
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            conversation.updated_at = timezone.now()
            conversation.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': {
                        'content': message.content,
                        'sender': message.sender.nickname,
                        'timestamp': message.timestamp.strftime('%H:%M')
                    }
                })
            return redirect('messaging:chat_view', conversation_id=conversation.id)
    else:
        form = ChatMessageForm()
    
    return render(request, 'messaging/chat.html', {
        'conversation': conversation,
        'messages': chat_messages,
        'other_user': other_user,
        'form': form
    })

@login_required
def stories_feed(request):
    """Feed de stories ativas"""
    # Stories das últimas 24 horas que ainda não expiraram
    active_stories = Story.objects.filter(
        is_active=True,
        expires_at__gt=timezone.now()
    ).select_related('user').order_by('-is_highlighted', '-created_at')
    
    # Agrupar stories por usuário
    stories_by_user = {}
    for story in active_stories:
        user_id = story.user.id
        if user_id not in stories_by_user:
            stories_by_user[user_id] = {
                'user': story.user,
                'stories': [],
                'unviewed_count': 0
            }
        stories_by_user[user_id]['stories'].append(story)
        
        # Verificar se o usuário já viu este story (apenas se estiver logado)
        if request.user.is_authenticated and not StoryView.objects.filter(story=story, viewer=request.user).exists():
            stories_by_user[user_id]['unviewed_count'] += 1
    
    context = {
        'stories_by_user': stories_by_user,
        'total_stories': active_stories.count(),
    }
    
    return render(request, 'messaging/stories_feed.html', context)

@login_required
def view_story(request, story_id):
    """Visualizar um story específico"""
    story = get_object_or_404(Story, id=story_id, is_active=True)
    
    # Verificar se o story não expirou
    if story.is_expired:
        messages.error(request, 'Este story expirou.')
        return redirect('messaging:stories_feed')
    
    # Registrar visualização se não for o próprio criador
    if story.user != request.user:
        StoryView.objects.get_or_create(story=story, viewer=request.user)
    
    # Buscar outros stories do mesmo usuário que ainda estão ativos
    user_stories = Story.objects.filter(
        user=story.user,
        is_active=True,
        expires_at__gt=timezone.now()
    ).order_by('created_at')
    
    # Encontrar o índice atual
    current_index = 0
    story_list = list(user_stories)
    for i, s in enumerate(story_list):
        if s.id == story.id:
            current_index = i
            break
    
    context = {
        'story': story,
        'user_stories': story_list,
        'current_index': current_index,
        'total_stories': len(story_list),
    }
    
    return render(request, 'messaging/view_story.html', context)

class CreateStoryView(CreateView):
    """Criar novo story"""
    model = Story
    form_class = StoryForm
    template_name = 'messaging/create_story.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        # Apenas empresas podem criar stories
        if self.request.user.user_type != 'company':
            messages.error(self.request, 'Apenas empresas podem criar stories.')
            return redirect('messaging:stories_feed')
        return super().form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Story criado com sucesso!')
        return '/messaging/stories/'

@login_required
def search_users(request):
    """Buscar usuários para iniciar conversa"""
    query = request.GET.get('q', '')
    users = []
    
    if query:
        users = User.objects.filter(
            Q(nickname__icontains=query) | 
            Q(first_name__icontains=query) |
            Q(email__icontains=query)
        ).exclude(id=request.user.id)[:10]
    
    return render(request, 'messaging/search_users.html', {
        'users': users,
        'query': query
    })

@login_required
def delete_story(request, story_id):
    """Deletar story próprio"""
    story = get_object_or_404(Story, id=story_id, user=request.user)
    story.delete()
    messages.success(request, 'Story deletado com sucesso!')
    return redirect('messaging:stories_feed')


# ==================== ÁREA SOCIAL DOS ESTUDANTES ====================

@login_required
def student_social_feed(request):
    """Feed social dos estudantes"""
    if request.user.user_type != 'student':
        messages.error(request, 'Área exclusiva para estudantes.')
        return redirect('core:home')
    
    # Filtros
    post_type = request.GET.get('type', 'all')
    search_query = request.GET.get('q', '')
    
    # Buscar posts
    posts = StudentPost.objects.filter(is_active=True).select_related('author').prefetch_related('likes', 'comments')
    
    if post_type != 'all':
        posts = posts.filter(post_type=post_type)
    
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    posts = posts.order_by('-created_at')
    
    # Processar tags para cada post
    for post in posts:
        if post.tags:
            post.tag_list = [tag.strip() for tag in post.tags.split(',') if tag.strip()]
        else:
            post.tag_list = []
    
    # Paginação
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas rápidas
    total_posts = StudentPost.objects.filter(is_active=True).count()
    total_students = User.objects.filter(user_type='student').count()
    total_study_groups = StudyGroup.objects.filter(is_active=True).count()
    
    context = {
        'page_obj': page_obj,
        'post_type': post_type,
        'search_query': search_query,
        'total_posts': total_posts,
        'total_students': total_students,
        'total_study_groups': total_study_groups,
    }
    
    return render(request, 'messaging/student_social_feed.html', context)

@login_required
def create_student_post(request):
    """Criar post na área social"""
    if request.user.user_type != 'student':
        messages.error(request, 'Área exclusiva para estudantes.')
        return redirect('core:home')
    
    if request.method == 'POST':
        form = StudentPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post criado com sucesso!')
            return redirect('messaging:student_social_feed')
    else:
        form = StudentPostForm()
    
    return render(request, 'messaging/create_student_post.html', {'form': form})

@login_required
def student_post_detail(request, post_id):
    """Detalhe de um post específico"""
    post = get_object_or_404(StudentPost, id=post_id, is_active=True)
    comments = post.comments.all().select_related('author')
    
    # Verificar se o usuário curtiu
    user_liked = False
    if request.user.is_authenticated:
        user_liked = PostLike.objects.filter(post=post, user=request.user).exists()
    
    # Processar comentário
    if request.method == 'POST' and request.user.user_type == 'student':
        content = request.POST.get('content')
        if content:
            PostComment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
            messages.success(request, 'Comentário adicionado!')
            return redirect('messaging:student_post_detail', post_id=post.id)
    
    context = {
        'post': post,
        'comments': comments,
        'user_liked': user_liked,
    }
    
    return render(request, 'messaging/student_post_detail.html', context)

@login_required
def toggle_post_like(request, post_id):
    """Curtir/descurtir post (AJAX)"""
    if request.user.user_type != 'student':
        return JsonResponse({'error': 'Área exclusiva para estudantes'}, status=403)
    
    post = get_object_or_404(StudentPost, id=post_id)
    like, created = PostLike.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes_count
    })

@login_required
def study_groups_list(request):
    """Lista de grupos de estudo"""
    if request.user.user_type != 'student':
        messages.error(request, 'Área exclusiva para estudantes.')
        return redirect('core:home')
    
    # Filtros
    subject = request.GET.get('subject', '')
    meeting_type = request.GET.get('meeting_type', '')
    university = request.GET.get('university', '')
    
    groups = StudyGroup.objects.filter(is_active=True).annotate(
        members_count=Count('members')
    ).select_related('creator')
    
    if subject:
        groups = groups.filter(subject__icontains=subject)
    if meeting_type:
        groups = groups.filter(meeting_type=meeting_type)
    if university:
        groups = groups.filter(university__icontains=university)
    
    groups = groups.order_by('-created_at')
    
    # Grupos que o usuário participa
    user_groups = request.user.study_groups.filter(is_active=True)
    
    context = {
        'groups': groups,
        'user_groups': user_groups,
        'subject': subject,
        'meeting_type': meeting_type,
        'university': university,
    }
    
    return render(request, 'messaging/study_groups_list.html', context)

@login_required
def create_study_group(request):
    """Criar grupo de estudos"""
    if request.user.user_type != 'student':
        messages.error(request, 'Área exclusiva para estudantes.')
        return redirect('core:home')
    
    if request.method == 'POST':
        form = StudyGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            group.members.add(request.user)  # Criador automaticamente vira membro
            messages.success(request, 'Grupo de estudos criado com sucesso!')
            return redirect('messaging:study_groups_list')
    else:
        form = StudyGroupForm()
    
    return render(request, 'messaging/create_study_group.html', {'form': form})

@login_required
def join_study_group(request, group_id):
    """Entrar em um grupo de estudos"""
    if request.user.user_type != 'student':
        return JsonResponse({'error': 'Área exclusiva para estudantes'}, status=403)
    
    group = get_object_or_404(StudyGroup, id=group_id, is_active=True)
    
    if group.is_full:
        return JsonResponse({'error': 'Grupo lotado'}, status=400)
    
    if request.user in group.members.all():
        return JsonResponse({'error': 'Você já faz parte deste grupo'}, status=400)
    
    group.members.add(request.user)
    
    return JsonResponse({
        'success': True,
        'message': f'Você entrou no grupo {group.name}!',
        'members_count': group.members_count
    })

@login_required
def leave_study_group(request, group_id):
    """Sair de um grupo de estudos"""
    if request.user.user_type != 'student':
        return JsonResponse({'error': 'Área exclusiva para estudantes'}, status=403)
    
    group = get_object_or_404(StudyGroup, id=group_id)
    
    if request.user not in group.members.all():
        return JsonResponse({'error': 'Você não faz parte deste grupo'}, status=400)
    
    group.members.remove(request.user)
    
    return JsonResponse({
        'success': True,
        'message': f'Você saiu do grupo {group.name}.',
        'members_count': group.members_count
    })

@login_required
def student_connections(request):
    """Lista de conexões do estudante"""
    if request.user.user_type != 'student':
        messages.error(request, 'Área exclusiva para estudantes.')
        return redirect('core:home')
    
    # Conexões aceitas
    accepted_connections = StudentConnection.objects.filter(
        Q(from_student=request.user, status='accepted') |
        Q(to_student=request.user, status='accepted')
    ).select_related('from_student', 'to_student')
    
    # Solicitações pendentes recebidas
    pending_requests = StudentConnection.objects.filter(
        to_student=request.user,
        status='pending'
    ).select_related('from_student')
    
    # Solicitações enviadas
    sent_requests = StudentConnection.objects.filter(
        from_student=request.user,
        status='pending'
    ).select_related('to_student')
    
    context = {
        'accepted_connections': accepted_connections,
        'pending_requests': pending_requests,
        'sent_requests': sent_requests,
    }
    
    return render(request, 'messaging/student_connections.html', context)

@login_required
def search_students(request):
    """Buscar outros estudantes"""
    if request.user.user_type != 'student':
        messages.error(request, 'Área exclusiva para estudantes.')
        return redirect('core:home')
    
    query = request.GET.get('q', '')
    course = request.GET.get('course', '')
    university = request.GET.get('university', '')
    
    students = User.objects.filter(user_type='student').exclude(id=request.user.id)
    
    if query:
        students = students.filter(
            Q(nickname__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    
    if course:
        students = students.filter(course__icontains=course)
    
    if university:
        students = students.filter(university__icontains=university)
    
    students = students[:20]  # Limite de resultados
    
    # Verificar status de conexão para cada estudante
    for student in students:
        student.connection_status = 'none'
        connection = StudentConnection.objects.filter(
            Q(from_student=request.user, to_student=student) |
            Q(from_student=student, to_student=request.user)
        ).first()
        
        if connection:
            student.connection_status = connection.status
    
    context = {
        'students': students,
        'query': query,
        'course': course,
        'university': university,
    }
    
    return render(request, 'messaging/search_students.html', context)

@login_required
def send_connection_request(request, user_id):
    """Enviar solicitação de conexão"""
    if request.user.user_type != 'student':
        messages.error(request, 'Área exclusiva para estudantes.')
        return redirect('core:home')
    
    target_user = get_object_or_404(User, id=user_id, user_type='student')
    
    if target_user == request.user:
        messages.error(request, 'Você não pode se conectar consigo mesmo.')
        return redirect('messaging:search_students')
    
    # Verificar se já existe uma conexão
    existing_connection = StudentConnection.objects.filter(
        Q(from_student=request.user, to_student=target_user) |
        Q(from_student=target_user, to_student=request.user)
    ).first()
    
    if existing_connection:
        if existing_connection.status == 'accepted':
            messages.info(request, f'Você já está conectado com {target_user.nickname}.')
        elif existing_connection.status == 'pending':
            messages.info(request, f'Solicitação para {target_user.nickname} já foi enviada.')
        return redirect('messaging:search_students')
    
    # Criar nova solicitação
    StudentConnection.objects.create(
        from_student=request.user,
        to_student=target_user,
        status='pending'
    )
    
    messages.success(request, f'Solicitação de conexão enviada para {target_user.nickname}!')
    return redirect('messaging:search_students')

@login_required
def student_connections(request):
    """Lista de conexões do estudante"""
    if request.user.user_type != 'student':
        messages.error(request, 'Área exclusiva para estudantes.')
        return redirect('core:home')
    
    # Conexões aceitas
    connections = StudentConnection.objects.filter(
        Q(from_student=request.user) | Q(to_student=request.user),
        status='accepted'
    ).select_related('from_student', 'to_student')
    
    # Solicitações pendentes recebidas
    pending_requests = StudentConnection.objects.filter(
        to_student=request.user,
        status='pending'
    ).select_related('from_student')
    
    # Solicitações enviadas
    sent_requests = StudentConnection.objects.filter(
        from_student=request.user,
        status='pending'
    ).select_related('to_student')
    
    context = {
        'connections': connections,
        'pending_requests': pending_requests,
        'sent_requests': sent_requests,
    }
    
    return render(request, 'messaging/student_connections.html', context)

@login_required
def join_study_group(request, group_id):
    """Participar de um grupo de estudos"""
    if request.user.user_type != 'student':
        messages.error(request, 'Área exclusiva para estudantes.')
        return redirect('core:home')
    
    group = get_object_or_404(StudyGroup, id=group_id, is_active=True)
    
    if request.user in group.members.all():
        messages.info(request, 'Você já faz parte deste grupo.')
        return redirect('messaging:study_groups_list')
    
    if group.members.count() >= group.max_members:
        messages.error(request, 'Este grupo já está lotado.')
        return redirect('messaging:study_groups_list')
    
    group.members.add(request.user)
    messages.success(request, f'Você agora faz parte do grupo "{group.name}"!')
    return redirect('messaging:study_groups_list')

@login_required
def leave_study_group(request, group_id):
    """Sair de um grupo de estudos"""
    if request.user.user_type != 'student':
        messages.error(request, 'Área exclusiva para estudantes.')
        return redirect('core:home')
    
    group = get_object_or_404(StudyGroup, id=group_id, is_active=True)
    
    if request.user not in group.members.all():
        messages.info(request, 'Você não faz parte deste grupo.')
        return redirect('messaging:study_groups_list')
    
    group.members.remove(request.user)
    messages.success(request, f'Você saiu do grupo "{group.name}".')
    return redirect('messaging:study_groups_list')

@login_required
def create_study_group(request):
    """Criar um novo grupo de estudos"""
    if request.user.user_type != 'student':
        messages.error(request, 'Área exclusiva para estudantes.')
        return redirect('core:home')
    
    if request.method == 'POST':
        # Processar dados do formulário
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        meeting_type = request.POST.get('meeting_type')
        max_members = request.POST.get('max_members')
        university = request.POST.get('university')
        semester = request.POST.get('semester')
        
        # Validações básicas
        if not all([name, subject, description, meeting_type, max_members]):
            messages.error(request, 'Todos os campos obrigatórios devem ser preenchidos.')
            return render(request, 'messaging/create_study_group.html')
        
        try:
            max_members = int(max_members)
            if max_members < 2 or max_members > 50:
                raise ValueError()
        except ValueError:
            messages.error(request, 'Número de membros deve ser entre 2 e 50.')
            return render(request, 'messaging/create_study_group.html')
        
        # Criar grupo
        group = StudyGroup.objects.create(
            creator=request.user,
            name=name,
            subject=subject,
            description=description,
            meeting_type=meeting_type,
            max_members=max_members,
            university=university or None,
            semester=semester or None,
        )
        
        # Adicionar criador como membro
        group.members.add(request.user)
        
        messages.success(request, f'Grupo "{name}" criado com sucesso!')
        return redirect('messaging:study_groups_list')
    
    return render(request, 'messaging/create_study_group.html')