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
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='photo')
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # Localização
    location = models.CharField(max_length=255, blank=True)
    
    # Tags
    hashtags = models.TextField(blank=True, help_text="Hashtags separadas por vírgula")
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.author.username} - {self.created_at.strftime('%d/%m/%Y')}"
    
    @property
    def likes_count(self):
        return self.likes.count()
    
    @property
    def comments_count(self):
        return self.comments.count()
    
    def get_hashtags_list(self):
        if self.hashtags:
            return [tag.strip() for tag in self.hashtags.split(',')]
        return []


class Like(models.Model):
    """Model para likes nos posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')
        
    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"


class Comment(models.Model):
    """Model para comentários nos posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Comentários aninhados (replies)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    class Meta:
        ordering = ['created_at']
        
    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"


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
    
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_listings')
    title = models.CharField(max_length=200)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    requirements = models.TextField()
    benefits = models.TextField(blank=True)
    
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='full_time')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS, default='entry')
    location = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=100, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Metadados
    tags = models.CharField(max_length=500, blank=True, help_text="Tags separadas por vírgula")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.company.username}"
    
    @property
    def applications_count(self):
        return self.applications.count()


class JobApplication(models.Model):
    """Candidaturas para vagas"""
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('reviewing', 'Em análise'),
        ('interview', 'Entrevista'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
    ]
    
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Feedback da empresa
    company_notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('job', 'applicant')
        ordering = ['-applied_at']
    
    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"