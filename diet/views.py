from django.shortcuts import render
from .forms import dietForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# Create your views here.

def add_Diet(request):
    """
    Adiciona um novo workout
    """
    if request.method == 'POST':
        form = dietForm(request.POST)
        if form.is_valid():
            diet = form.save()
            
            response = redirect('add_exercise', diet_id=diet.id)  # Corrigido: adicionar workout_id
            response.set_cookie('success_message', 'Dieta criada com sucesso!!', max_age=5)
            request.session['diet_id'] = diet.id
            return response
    else:
        form = dietForm()
    
    context = {'form': form}
    return render(request, 'add_diet.html', context)
