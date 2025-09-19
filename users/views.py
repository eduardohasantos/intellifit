from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        birthdate = request.POST.get('birthdate')

        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse('Já existe um usuário com esse username')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return HttpResponse('usuário cadastrado com sucesso')

def login(request):
    return render(request, 'login.html')