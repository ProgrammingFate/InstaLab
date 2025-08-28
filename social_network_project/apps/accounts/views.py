from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import UserRegistrationForm, UserLoginForm

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # cria usuário
            messages.success(request, 'Cadastro realizado com sucesso! Faça login.')
            return redirect('accounts:login')  # vai para login
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bem-vindo(a), {user.nickname or user.username}!')
            return redirect('core:home')  # Redirecionando para a home
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', { 'user': request.user })

def logout_view(request):
    logout(request)
    return redirect('accounts:login')  # namespace corrigido