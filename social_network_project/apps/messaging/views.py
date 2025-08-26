from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Q, Max
from django.contrib import messages
from .models import Conversation, ChatMessage, Story, StoryView
from .forms import StoryForm, ChatMessageForm

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
            return redirect('conversations_list')
    
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
            return redirect('chat_view', conversation_id=conversation.id)
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
    # Stories das últimas 24 horas
    active_stories = Story.objects.filter(
        is_active=True,
        expires_at__gt=timezone.now()
    ).select_related('user').order_by('-created_at')
    
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
        
        # Verificar se o usuário já viu este story
        if not StoryView.objects.filter(story=story, viewer=request.user).exists():
            stories_by_user[user_id]['unviewed_count'] += 1
    
    return render(request, 'messaging/stories_feed.html', {
        'stories_by_user': stories_by_user
    })

@login_required
def view_story(request, story_id):
    """Visualizar um story específico"""
    story = get_object_or_404(Story, id=story_id, is_active=True)
    
    # Registrar visualização se não for o próprio criador
    if story.user != request.user:
        StoryView.objects.get_or_create(story=story, viewer=request.user)
    
    # Buscar outros stories do mesmo usuário
    user_stories = Story.objects.filter(
        user=story.user,
        is_active=True,
        expires_at__gt=timezone.now()
    ).order_by('created_at')
    
    return render(request, 'messaging/view_story.html', {
        'story': story,
        'user_stories': user_stories,
        'current_index': list(user_stories).index(story)
    })

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
            return redirect('stories_feed')
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
    return redirect('stories_feed')