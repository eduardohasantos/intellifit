from django.shortcuts import render
from .forms import DietForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from users.views import dashboard

# Sugestão de correção na views.py:
# A sua view 'add_Diet' está importando 'dietForm' (com 'd' minúsculo)
# Mude a importação para usar a classe que definimos acima, que chamei de DietForm (com 'D' maiúsculo, convenção Python para classes)
# from .forms import DietForm 
# e na views.py use: form = DietForm(request.POST)


def add_Diet(request):
    """
    Adiciona um novo workout
    """
    if request.method == 'POST':
        form = DietForm(request.POST)
        if form.is_valid():
            diet = form.save()
            
            #response = redirect('gerenciar_dietas', diet_id=diet.id)
            response = redirect('dashboard') 
            response.set_cookie('success_message', 'Dieta criada com sucesso!!', max_age=5)
            request.session['diet_id'] = diet.id
            return response
    else:
        form = DietForm()
    
    context = {'form': form}
    return render(request, 'add_diet.html', context)
