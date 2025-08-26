from django import forms
from .models import Story, ChatMessage

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'content', 'image', 'story_type']
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
            })
        }
        labels = {
            'title': 'Título',
            'content': 'Descrição',
            'image': 'Imagem (opcional)',
            'story_type': 'Tipo do Story'
        }

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
