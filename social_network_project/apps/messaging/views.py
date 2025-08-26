from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.accounts.models import Message  # usando o modelo Message definido em accounts

User = get_user_model()

class MessageListView(ListView):
    model = Message
    template_name = "messaging/message_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        # Lista mensagens do usuário logado (enviadas ou recebidas)
        return Message.objects.filter(
            timestamp__lte=timezone.now()
        ).filter(
            sender=self.request.user
        ) | Message.objects.filter(
            timestamp__lte=timezone.now(),
            receiver=self.request.user
        ).order_by('-timestamp')

class ChatView(TemplateView):
    template_name = "messaging/chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        other_user_id = self.request.GET.get('u')
        if other_user_id:
            other = get_object_or_404(User, pk=other_user_id)
            context['other_user'] = other
            context['messages'] = Message.objects.filter(
                sender__in=[self.request.user, other],
                receiver__in=[self.request.user, other]
            ).order_by('timestamp')
        else:
            context['messages'] = []
        return context

@login_required
def chat_view(request):  # função alternativa (se quiser usar no lugar da class-based)
    other_user_id = request.GET.get('u')
    messages_qs = Message.objects.none()
    other = None
    if other_user_id:
        other = get_object_or_404(User, pk=other_user_id)
        messages_qs = Message.objects.filter(
            sender__in=[request.user, other],
            receiver__in=[request.user, other]
        ).order_by('timestamp')
    return render(request, 'messaging/chat.html', {
        'messages': messages_qs,
        'other_user': other
    })

@login_required
def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        receiver_id = request.POST.get('receiver')
        if content and receiver_id:
            receiver = get_object_or_404(User, pk=receiver_id)
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
        # Redireciona de volta para o chat com o mesmo usuário
        return redirect(f"/messaging/chat/?u={receiver_id}") if receiver_id else redirect('chat')
    return redirect('chat')