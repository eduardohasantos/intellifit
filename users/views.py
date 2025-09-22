from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm
from django.contrib.auth import logout

def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.add_message(request, constants.ERROR, "Email já cadastrado")
            return render(request, 'register.html', {
                'username': username,
            })
        
        if User.objects.filter(username=username).exists():
            messages.add_message(request, constants.ERROR, "Nome já cadastrado")
            return render(request, 'register.html', {
                'email': email,
            })
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Usuário cadastrado com sucesso!")
        return redirect('login')

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login_django(request, user)

            return redirect('dashboard')
        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
            return render(request, 'login.html', {
                'username': username,
            })
        
@login_required(login_url = "/auth/login/")
def dashboard(request):
    return render(request, 'dashboard.html')

def home(request):
    return render(request, "home.html")

@login_required(login_url="/auth/login/")
def logout_view(request):
    logout(request)
    messages.success(request, "Logout realizado com sucesso!")
    return redirect('login')

@login_required(login_url="/auth/login/")
def edit_account(request):
    if request.method == 'POST':
        # Passamos 'instance=request.user' para que o formulário saiba qual usuário editar
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('dashboard')
    else:
        # Se não for POST, apenas exibe o formulário com os dados atuais do usuário
        form = UserEditForm(instance=request.user)

    return render(request, 'edit_account.html', {'form': form})

@login_required(login_url="/auth/login/")
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Sua conta foi excluída com sucesso.')
        return redirect('home') # Redireciona para a página inicial após excluir

    # Se for GET, apenas mostra a página de confirmação
    return render(request, 'delete_account.html')