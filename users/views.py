from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants

def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        birthdate = request.POST.get('birthdate')

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

        return HttpResponse('usuário cadastrado com sucesso')

def login(request):
    return render(request, 'login.html')