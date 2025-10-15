from django import forms
from .models import JobListing, JobApplication, JobCategory, Post, Comment

class JobListingForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = [
            'title', 'category', 'description', 'requirements', 'benefits',
            'job_type', 'experience_level', 'location', 'salary_range', 'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Desenvolvedor Frontend React'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva a vaga, responsabilidades e o que oferece...'
            }),
            'requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Quais são os requisitos necessários?'
            }),
            'benefits': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Quais são os benefícios oferecidos?'
            }),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'experience_level': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: São Paulo, SP ou Remoto'
            }),
            'salary_range': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: R$ 2.000 - R$ 3.000'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: React, TypeScript, Frontend (separadas por vírgula)'
            }),
        }
        labels = {
            'title': 'Título da Vaga',
            'category': 'Categoria',
            'description': 'Descrição',
            'requirements': 'Requisitos',
            'benefits': 'Benefícios',
            'job_type': 'Tipo de Vaga',
            'experience_level': 'Nível de Experiência',
            'location': 'Localização',
            'salary_range': 'Faixa Salarial',
            'tags': 'Tags/Tecnologias',
        }

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Conte um pouco sobre você, sua experiência e por que tem interesse nesta vaga...'
            }),
            'resume': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            })
        }
        labels = {
            'cover_letter': 'Carta de Apresentação',
            'resume': 'Currículo (PDF, DOC ou DOCX)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cover_letter'].required = True
        self.fields['resume'].required = False

class JobFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=JobCategory.objects.all(),
        required=False,
        empty_label="Todas as categorias",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por título, empresa ou tecnologia...'
        })
    )
    remote_only = forms.BooleanField(
        required=False,
        label='Apenas vagas remotas',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class PostForm(forms.ModelForm):
    """Formulário para criar posts"""
    
    class Meta:
        model = Post
        fields = ['content', 'image', 'video', 'post_type', 'location', 'hashtags']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'O que você está pensando?',
                'rows': 3,
                'style': 'resize: none;'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'video': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'video/*'
            }),
            'post_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adicionar localização...'
            }),
            'hashtags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '#hashtag1, #hashtag2, #hashtag3'
            })
        }


class CommentForm(forms.ModelForm):
    """Formulário para comentários"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adicione um comentário...',
                'style': 'border: none; background: transparent;'
            })
        }
