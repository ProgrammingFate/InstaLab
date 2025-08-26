from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.nickname or self.author.username} - {self.created_at}'

class JobCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    icon = models.CharField(max_length=10, default='💼')  # Emoji icon
    
    class Meta:
        verbose_name_plural = "Job Categories"
    
    def __str__(self):
        return self.name

class JobListing(models.Model):
    STATUS_CHOICES = [
        ('active', 'Ativa'),
        ('closed', 'Fechada'),
        ('draft', 'Rascunho'),
    ]
    
    PRIORITY_CHOICES = [
        ('normal', 'Normal'),
        ('urgent', 'Urgente'),
        ('featured', 'Destaque'),
    ]
    
    # Informações básicas
    title = models.CharField(max_length=200)
    company = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_listings')
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    
    # Detalhes da vaga
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    spots_available = models.PositiveIntegerField(default=1)
    location = models.CharField(max_length=100, blank=True)
    remote_work = models.BooleanField(default=False)
    
    # Status e configurações
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)
    
    # Tags
    tags = models.CharField(max_length=200, blank=True, help_text="Separe as tags com vírgulas")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.company.company_name or self.company.nickname}"
    
    def get_tags_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def spots_remaining(self):
        applications_count = self.applications.filter(status='applied').count()
        return max(0, self.spots_available - applications_count)
    
    def is_deadline_passed(self):
        if self.deadline:
            return timezone.now() > self.deadline
        return False

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Candidatado'),
        ('reviewing', 'Em Análise'),
        ('accepted', 'Aceito'),
        ('rejected', 'Rejeitado'),
        ('withdrawn', 'Retirado'),
    ]
    
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_applications')
    
    # Informações da candidatura
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='applied')
    
    # Timestamps
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Notas internas (visível apenas para a empresa)
    internal_notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['job', 'applicant']  # Um usuário só pode se candidatar uma vez por vaga
        ordering = ['-applied_at']
    
    def __str__(self):
        return f"{self.applicant.nickname} - {self.job.title}"