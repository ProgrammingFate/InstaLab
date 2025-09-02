from django import forms
from .models import Story, ChatMessage, StudentPost, StudyGroup
from apps.core.models import JobListing

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'content', 'image', 'story_type', 'related_job', 'external_link', 'is_highlighted']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título do story...',
                'maxlength': 100
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Conte mais sobre...',
                'rows': 4
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'story_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'related_job': forms.Select(attrs={
                'class': 'form-select'
            }),
            'external_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://...'
            }),
            'is_highlighted': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'title': 'Título',
            'content': 'Descrição',
            'image': 'Imagem (opcional)',
            'story_type': 'Tipo do Story',
            'related_job': 'Vaga Relacionada (opcional)',
            'external_link': 'Link Externo (opcional)',
            'is_highlighted': 'Story Destacado'
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.user_type == 'company':
            # Filtrar apenas vagas da empresa
            self.fields['related_job'].queryset = JobListing.objects.filter(company=user)
        else:
            self.fields['related_job'].queryset = JobListing.objects.none()

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite sua mensagem...',
                'autocomplete': 'off'
            })
        }
        labels = {
            'content': ''
        }

class StudentPostForm(forms.ModelForm):
    class Meta:
        model = StudentPost
        fields = ['title', 'content', 'image', 'post_type', 'tags', 'study_subject', 'max_participants']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título do seu post...',
                'maxlength': 200
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Compartilhe seus pensamentos, dúvidas ou conquistas...',
                'rows': 5
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'post_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: programação, python, web, estudos (separadas por vírgula)'
            }),
            'study_subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Cálculo I, Algoritmos, Física...'
            }),
            'max_participants': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 2,
                'max': 50
            })
        }
        labels = {
            'title': 'Título',
            'content': 'Conteúdo',
            'image': 'Imagem (opcional)',
            'post_type': 'Tipo do Post',
            'tags': 'Tags',
            'study_subject': 'Matéria (para grupos de estudo)',
            'max_participants': 'Máx. Participantes (para grupos de estudo)'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Campos condicionais baseados no tipo do post
        self.fields['study_subject'].required = False
        self.fields['max_participants'].required = False

class StudyGroupForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ['name', 'description', 'subject', 'max_members', 'meeting_type', 'university', 'semester']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do grupo de estudos...',
                'maxlength': 100
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descreva os objetivos e metodologia do grupo...',
                'rows': 4
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Cálculo I, Programação Web, Física II...',
                'maxlength': 100
            }),
            'max_members': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 2,
                'max': 50,
                'value': 10
            }),
            'meeting_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'university': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sua universidade (opcional)...'
            }),
            'semester': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 3º semestre, 2024.2...'
            })
        }
        labels = {
            'name': 'Nome do Grupo',
            'description': 'Descrição',
            'subject': 'Matéria/Assunto',
            'max_members': 'Máximo de Membros',
            'meeting_type': 'Tipo de Encontro',
            'university': 'Universidade (opcional)',
            'semester': 'Semestre (opcional)'
        }
