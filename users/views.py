from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required

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

        messages.sucess(request, "Usuário cadastrado com sucesso!")
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