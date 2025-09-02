from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Digite sua senha'
    }))
    password2 = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirme sua senha'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'company_name', 'company_description', 
                 'company_instagram', 'course', 'university', 'semester']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seu nome de usuário'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'seu@email.com'
            }),
            'user_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da sua empresa/organização'
            }),
            'company_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Descreva sua empresa júnior:\n\n• Qual é a missão e visão da empresa?\n• Em quais áreas vocês atuam? (marketing, desenvolvimento, consultoria, etc.)\n• Quantos membros tem a equipe?\n• Alguns projetos ou clientes importantes\n• Valores e cultura da empresa\n\nExemplo: "Somos uma empresa júnior de engenharia com foco em soluções tecnológicas. Atuamos há 5 anos no mercado, desenvolvendo projetos de automação e consultoria para pequenas e médias empresas..."'
            }),
            'company_instagram': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '@suaempresajr (opcional)'
            }),
            'course': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Ciência da Computação'
            }),
            'university': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: USP, UFMG, PUC...',
                'list': 'universities-list',
                'autocomplete': 'off'
            }),
            'semester': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 5º semestre'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Labels customizados
        self.fields['company_name'].label = 'Nome da Empresa Júnior'
        self.fields['company_description'].label = 'Sobre a Empresa Júnior'
        self.fields['company_instagram'].label = 'Instagram da Empresa (opcional)'
        self.fields['course'].label = 'Curso'
        self.fields['university'].label = 'Universidade/Faculdade'
        self.fields['semester'].label = 'Período/Semestre'
        
        # Campos condicionais baseados no tipo de usuário
        self.fields['company_name'].required = False
        self.fields['company_description'].required = False
        self.fields['company_instagram'].required = False
        self.fields['course'].required = False
        self.fields['university'].required = False
        self.fields['semester'].required = False

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('As senhas não coincidem.')
        if password1 and len(password1) < 8:
            raise forms.ValidationError('A senha deve ter no mínimo 8 caracteres.')
        return password2

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        
        # Validações específicas para empresa
        if user_type == 'company':
            if not cleaned_data.get('company_name'):
                raise forms.ValidationError('Nome da empresa é obrigatório para empresas.')
        
        # Validações específicas para estudante
        elif user_type == 'student':
            if not cleaned_data.get('course'):
                raise forms.ValidationError('Curso é obrigatório para estudantes.')
            if not cleaned_data.get('university'):
                raise forms.ValidationError('Universidade é obrigatória para estudantes.')
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Gera nickname único baseado no username
        base = self.cleaned_data['username']
        nickname = base
        i = 1
        while User.objects.filter(nickname__iexact=nickname).exists():
            i += 1
            nickname = f"{base}{i}"
        user.nickname = nickname
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'company_name', 'company_description', 
                 'company_instagram', 'course', 'university', 'semester', 'bio', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seu nome de usuário'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'seu@email.com'
            }),
            'user_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da sua empresa/organização'
            }),
            'company_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Descreva sua empresa júnior'
            }),
            'company_instagram': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '@suaempresajr (opcional)'
            }),
            'course': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Ciência da Computação'
            }),
            'university': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: USP, UFMG, PUC...'
            }),
            'semester': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 5º semestre'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Conte um pouco sobre você...'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Labels customizados
        self.fields['company_name'].label = 'Nome da Empresa Júnior'
        self.fields['company_description'].label = 'Sobre a Empresa Júnior'
        self.fields['company_instagram'].label = 'Instagram da Empresa (opcional)'
        self.fields['course'].label = 'Curso'
        self.fields['university'].label = 'Universidade/Faculdade'
        self.fields['semester'].label = 'Período/Semestre'
        self.fields['bio'].label = 'Biografia'
        self.fields['avatar'].label = 'Foto de Perfil'
        
        # Campos condicionais baseados no tipo de usuário
        self.fields['company_name'].required = False
        self.fields['company_description'].required = False
        self.fields['company_instagram'].required = False
        self.fields['course'].required = False
        self.fields['university'].required = False
        self.fields['semester'].required = False
        self.fields['bio'].required = False
        self.fields['avatar'].required = False

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        
        # Validações específicas para empresa
        if user_type == 'company':
            if not cleaned_data.get('company_name'):
                raise forms.ValidationError('Nome da empresa é obrigatório para empresas.')
        
        # Validações específicas para estudante
        elif user_type == 'student':
            if not cleaned_data.get('course'):
                raise forms.ValidationError('Curso é obrigatório para estudantes.')
            if not cleaned_data.get('university'):
                raise forms.ValidationError('Universidade é obrigatória para estudantes.')
        
        return cleaned_data

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuário', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Seu nome de usuário'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Sua senha'
    }), label='Senha')