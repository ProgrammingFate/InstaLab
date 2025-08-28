from django import forms
from .models import JobListing, JobApplication, JobCategory

class JobListingForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = [
            'title', 'category', 'description', 'requirements', 'responsibilities',
            'salary_min', 'salary_max', 'spots_available', 'location', 'remote_work',
            'deadline', 'tags', 'priority'
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
            'responsibilities': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Quais serão as principais responsabilidades?'
            }),
            'salary_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '800 (opcional)',
                'step': '0.01'
            }),
            'salary_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1200 (opcional)',
                'step': '0.01'
            }),
            'spots_available': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: São Paulo, SP ou Remoto'
            }),
            'remote_work': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'deadline': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: React, TypeScript, Frontend (separadas por vírgula)'
            }),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Título da Vaga',
            'category': 'Categoria',
            'description': 'Descrição',
            'requirements': 'Requisitos',
            'responsibilities': 'Responsabilidades',
            'salary_min': 'Salário Mínimo (R$ - Opcional)',
            'salary_max': 'Salário Máximo (R$ - Opcional)',
            'spots_available': 'Número de Vagas',
            'location': 'Localização',
            'remote_work': 'Trabalho Remoto',
            'deadline': 'Prazo Limite',
            'tags': 'Tags/Tecnologias',
            'priority': 'Prioridade',
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
