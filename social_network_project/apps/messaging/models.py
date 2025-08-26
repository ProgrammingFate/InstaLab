# apps/messaging/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class Conversation(models.Model):
    """Conversa entre dois usuários"""
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        users = list(self.participants.all())
        if len(users) >= 2:
            return f"Chat entre {users[0].nickname} e {users[1].nickname}"
        return f"Chat {self.id}"
    
    @property
    def last_message(self):
        return self.messages.last()

class ChatMessage(models.Model):
    """Mensagem individual em uma conversa"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    message_type = models.CharField(max_length=20, choices=[
        ('text', 'Texto'),
        ('image', 'Imagem'),
        ('file', 'Arquivo'),
    ], default='text')
    
    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.sender.nickname}: {self.content[:50]}...'

class Story(models.Model):
    """Stories das empresas para mostrar vagas, projetos, etc."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stories')
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='stories/', blank=True, null=True)
    story_type = models.CharField(max_length=20, choices=[
        ('job', 'Nova Vaga'),
        ('project', 'Novo Projeto'),
        ('identity', 'Nova Identidade'),
        ('announcement', 'Anúncio'),
        ('achievement', 'Conquista'),
    ], default='announcement')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Stories'
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Stories expiram em 24 horas
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"{self.user.nickname} - {self.title}"

class StoryView(models.Model):
    """Visualizações dos stories"""
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='views')
    viewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['story', 'viewer']
    
    def __str__(self):
        return f"{self.viewer.nickname} viu story de {self.story.user.nickname}"
