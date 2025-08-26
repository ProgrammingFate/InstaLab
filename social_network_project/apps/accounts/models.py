from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('student', 'Estudante'),
        ('company', 'Empresa Júnior / Organização'),
    ]
    
    nickname = models.CharField(max_length=30, unique=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    
    # Campos específicos para empresas/organizações
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    company_instagram = models.CharField(max_length=100, blank=True, null=True, help_text="Ex: @empresajr")
    
    # Campos específicos para estudantes
    course = models.CharField(max_length=100, blank=True, null=True)
    university = models.CharField(max_length=100, blank=True, null=True)
    semester = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nickname or self.username
    
    def is_company(self):
        return self.user_type == 'company'
    
    def is_student(self):
        return self.user_type == 'student'

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"Perfil de {self.user.nickname}" if self.user.nickname else self.user.username

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

# Modelo de mensagem simples (direta) corrigido
class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:30]}"
