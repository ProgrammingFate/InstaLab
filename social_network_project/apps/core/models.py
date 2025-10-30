from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Post(models.Model):
    """Model para posts do feed estilo Instagram"""
    POST_TYPES = [
        ('photo', 'Foto'),
        ('video', 'Vídeo'),
        ('text', 'Texto'),
        ('job', 'Vaga'),
        ('project', 'Projeto'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', db_index=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='photo', db_index=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, db_index=True)
    
    # Localização
    location = models.CharField(max_length=255, blank=True)
    
    # Tags
    hashtags = models.TextField(blank=True, help_text="Hashtags separadas por vírgula")
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at', 'is_active']),
            models.Index(fields=['author', '-created_at']),
        ]
        
    def __str__(self):
        return f"{self.author.username} - {self.created_at.strftime('%d/%m/%Y')}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        # Validar que pelo menos um conteúdo está presente
        if not any([self.content, self.image, self.video]):
            raise ValidationError('O post deve ter pelo menos um conteúdo (texto, imagem ou vídeo).')
        
        # Validar tipo de post vs conteúdo
        if self.post_type == 'photo' and not self.image:
            raise ValidationError('Posts de tipo "Foto" devem ter uma imagem.')
        if self.post_type == 'video' and not self.video:
            raise ValidationError('Posts de tipo "Vídeo" devem ter um vídeo.')
    
    @property
    def likes_count(self):
        return self.likes.count()
    
    @property
    def comments_count(self):
        return self.comments.count()
    
    def get_hashtags_list(self):
        if self.hashtags:
            return [tag.strip() for tag in self.hashtags.split(',') if tag.strip()]
        return []
    
    def toggle_active(self):
        """Toggle the active status of the post"""
        self.is_active = not self.is_active
        self.save(update_fields=['is_active'])


class Like(models.Model):
    """Model para likes nos posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        unique_together = ('user', 'post')
        indexes = [
            models.Index(fields=['post', '-created_at']),
        ]
        
    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"


class Comment(models.Model):
    """Model para comentários nos posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', db_index=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Comentários aninhados (replies)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'created_at']),
        ]
        
    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.content or not self.content.strip():
            raise ValidationError('O comentário não pode estar vazio.')
        if len(self.content) > 500:
            raise ValidationError('O comentário não pode ter mais de 500 caracteres.')


class Follow(models.Model):
    """Model para sistema de seguir usuários"""
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')
        
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


class Story(models.Model):
    """Model para Stories estilo Instagram"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feed_stories')
    image = models.ImageField(upload_to='stories/', blank=True, null=True)
    video = models.FileField(upload_to='stories/videos/', blank=True, null=True)
    text_content = models.TextField(blank=True)
    
    # Configurações
    background_color = models.CharField(max_length=7, default='#000000')
    text_color = models.CharField(max_length=7, default='#FFFFFF')
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    # Link externo (para empresas)
    external_link = models.URLField(blank=True, null=True)
    link_text = models.CharField(max_length=50, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Stories"
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    @property
    def is_active(self):
        return not self.is_expired()
    
    def __str__(self):
        return f"Story by {self.user.username} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"


class StoryView(models.Model):
    """Model para visualizações de stories"""
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feed_story_views')
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('story', 'user')


class JobCategory(models.Model):
    """Categorias de vagas"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name_plural = "Job Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class JobListing(models.Model):
    """Vagas de trabalho/estágio"""
    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('paused', 'Pausado'),
        ('closed', 'Fechado'),
    ]
    
    EXPERIENCE_LEVELS = [
        ('entry', 'Iniciante'),
        ('junior', 'Júnior'),
        ('mid', 'Pleno'),
        ('senior', 'Sênior'),
    ]
    
    JOB_TYPES = [
        ('internship', 'Estágio'),
        ('part_time', 'Meio período'),
        ('full_time', 'Tempo integral'),
        ('contract', 'Contrato'),
        ('freelance', 'Freelance'),
    ]
    
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_listings', db_index=True)
    title = models.CharField(max_length=200, db_index=True)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)
    description = models.TextField()
    requirements = models.TextField()
    benefits = models.TextField(blank=True)
    
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='full_time', db_index=True)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS, default='entry')
    location = models.CharField(max_length=255, db_index=True)
    salary_range = models.CharField(max_length=100, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Metadados
    tags = models.CharField(max_length=500, blank=True, help_text="Tags separadas por vírgula")
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['company', 'status']),
            models.Index(fields=['category', 'status', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.company.username}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.title or not self.title.strip():
            raise ValidationError('O título não pode estar vazio.')
        if len(self.title) < 10:
            raise ValidationError('O título deve ter pelo menos 10 caracteres.')
        if len(self.description) < 50:
            raise ValidationError('A descrição deve ter pelo menos 50 caracteres.')
    
    @property
    def applications_count(self):
        return self.applications.count()
    
    @property
    def is_active(self):
        return self.status == 'active'
    
    def is_deadline_passed(self):
        """Check if job is still accepting applications"""
        return self.status == 'closed'
    
    def close(self):
        """Close the job listing"""
        self.status = 'closed'
        self.save(update_fields=['status'])
    
    def pause(self):
        """Pause the job listing"""
        self.status = 'paused'
        self.save(update_fields=['status'])
    
    def activate(self):
        """Activate the job listing"""
        self.status = 'active'
        self.save(update_fields=['status'])


class JobApplication(models.Model):
    """Candidaturas para vagas"""
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('reviewing', 'Em análise'),
        ('interview', 'Entrevista'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
    ]
    
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE, related_name='applications', db_index=True)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications', db_index=True)
    
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    applied_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Feedback da empresa
    company_notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('job', 'applicant')
        ordering = ['-applied_at']
        indexes = [
            models.Index(fields=['job', 'status']),
            models.Index(fields=['applicant', '-applied_at']),
        ]
    
    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.cover_letter or not self.cover_letter.strip():
            raise ValidationError('A carta de apresentação não pode estar vazia.')
        if len(self.cover_letter) < 100:
            raise ValidationError('A carta de apresentação deve ter pelo menos 100 caracteres.')
    
    def approve(self):
        """Approve the application"""
        self.status = 'approved'
        self.save(update_fields=['status'])
    
    def reject(self):
        """Reject the application"""
        self.status = 'rejected'
        self.save(update_fields=['status'])
    
    def set_interview(self):
        """Set application status to interview"""
        self.status = 'interview'
        self.save(update_fields=['status'])