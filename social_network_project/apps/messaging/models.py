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
    title = models.CharField(max_length=100, help_text="Título do story")
    content = models.TextField(help_text="Conteúdo principal do story")
    image = models.ImageField(upload_to='stories/', blank=True, null=True, help_text="Imagem do story")
    story_type = models.CharField(max_length=20, choices=[
        ('job', 'Nova Vaga'),
        ('project', 'Novo Projeto'),
        ('company_update', 'Atualização da Empresa'),
        ('announcement', 'Anúncio'),
        ('achievement', 'Conquista'),
        ('event', 'Evento'),
        ('culture', 'Cultura da Empresa'),
    ], default='announcement')
    
    # Link relacionado (opcional)
    related_job = models.ForeignKey('core.JobListing', on_delete=models.CASCADE, blank=True, null=True, 
                                    help_text="Vaga relacionada ao story")
    external_link = models.URLField(blank=True, null=True, help_text="Link externo relacionado")
    
    # Configurações de tempo
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(help_text="Quando o story expira")
    is_active = models.BooleanField(default=True)
    
    # Configurações de visibilidade
    is_highlighted = models.BooleanField(default=False, help_text="Story destacado (fica no topo)")
    
    class Meta:
        ordering = ['-is_highlighted', '-created_at']
        verbose_name_plural = 'Stories'
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Stories expiram em 24 horas por padrão
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    @property
    def time_left(self):
        """Retorna o tempo restante em horas"""
        if self.is_expired:
            return 0
        diff = self.expires_at - timezone.now()
        return max(0, diff.total_seconds() / 3600)
    
    @property
    def views_count(self):
        return self.views.count()
    
    def __str__(self):
        return f"{self.user.company_name or self.user.nickname} - {self.title}"

class StoryView(models.Model):
    """Visualizações dos stories"""
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='views')
    viewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['story', 'viewer']
    
    def __str__(self):
        return f"{self.viewer.nickname} viu story de {self.story.user.nickname}"


# ==================== ÁREA SOCIAL DOS ESTUDANTES ====================

class StudentPost(models.Model):
    """Posts dos estudantes na área social"""
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_posts')
    title = models.CharField(max_length=200, help_text="Título do post")
    content = models.TextField(help_text="Conteúdo do post")
    image = models.ImageField(upload_to='student_posts/', blank=True, null=True)
    
    post_type = models.CharField(max_length=20, choices=[
        ('help', 'Pedido de Ajuda'),
        ('share', 'Compartilhamento'),
        ('project', 'Projeto Pessoal'),
        ('achievement', 'Conquista'),
        ('study_group', 'Grupo de Estudos'),
        ('networking', 'Networking'),
        ('discussion', 'Discussão'),
    ], default='discussion')
    
    tags = models.CharField(max_length=500, blank=True, help_text="Tags separadas por vírgula")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # Campos específicos para grupos de estudo
    study_subject = models.CharField(max_length=100, blank=True, help_text="Matéria de estudo")
    max_participants = models.PositiveIntegerField(null=True, blank=True, help_text="Máximo de participantes")
    
    class Meta:
        ordering = ['-created_at']
    
    @property
    def likes_count(self):
        return self.likes.count()
    
    @property
    def comments_count(self):
        return self.comments.count()
    
    def __str__(self):
        return f"{self.author.nickname} - {self.title}"


class PostLike(models.Model):
    """Curtidas nos posts dos estudantes"""
    post = models.ForeignKey(StudentPost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['post', 'user']


class PostComment(models.Model):
    """Comentários nos posts dos estudantes"""
    post = models.ForeignKey(StudentPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(help_text="Conteúdo do comentário")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.author.nickname} comentou em {self.post.title}"


class StudentConnection(models.Model):
    """Conexões entre estudantes (como amizades)"""
    from_student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_connections')
    to_student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_connections')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pendente'),
        ('accepted', 'Aceito'),
        ('rejected', 'Rejeitado'),
        ('blocked', 'Bloqueado'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['from_student', 'to_student']
    
    def __str__(self):
        return f"{self.from_student.nickname} -> {self.to_student.nickname} ({self.status})"


class StudyGroup(models.Model):
    """Grupos de estudo criados pelos estudantes"""
    name = models.CharField(max_length=100, help_text="Nome do grupo")
    description = models.TextField(help_text="Descrição do grupo")
    subject = models.CharField(max_length=100, help_text="Matéria/Assunto principal")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_study_groups')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='study_groups', blank=True)
    max_members = models.PositiveIntegerField(default=10, help_text="Máximo de membros")
    
    meeting_type = models.CharField(max_length=20, choices=[
        ('online', 'Online'),
        ('presential', 'Presencial'),
        ('hybrid', 'Híbrido'),
    ], default='online')
    
    university = models.CharField(max_length=200, blank=True, help_text="Universidade (opcional)")
    semester = models.CharField(max_length=50, blank=True, help_text="Semestre (opcional)")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    @property
    def members_count(self):
        return self.members.count()
    
    @property
    def is_full(self):
        return self.members_count >= self.max_members
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
