from django.http import Http404
def diet_detail(request, diet_id):
    try:
        dieta = DietPersist.objects.prefetch_related('meals').get(id=diet_id, user=request.user)
    except DietPersist.DoesNotExist:
        raise Http404('Dieta não encontrada')
    total_calorias = sum(meal.calories for meal in dieta.meals.all())
    return render(request, 'diet_detail.html', {'dieta': dieta, 'total_calorias': total_calorias})
from django.shortcuts import render
from .forms import DietForm,DietMealFormSet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from users.views import dashboard
from .models import DietPersist, DietMeal
from django.contrib.auth.decorators import login_required



def diet_page(request):
    if request.user.is_authenticated:
        dietas = DietPersist.objects.filter(user=request.user).prefetch_related('meals')
    else:
        dietas = DietPersist.objects.none()
    context = {
        'dietas': dietas
    }
    return render(request, 'diet.html', context)

def add_diet(request):
    if request.method == 'POST':
        form = DietForm(request.POST)
        if form.is_valid():
            diet = form.save(commit=False)
            diet.user = request.user
            diet.save()
            # Processar os pratos
            food_names = request.POST.getlist('food_name[]')
            food_calories = request.POST.getlist('food_calories[]')
            for name, calories in zip(food_names, food_calories):
                if name and calories:
                    DietMeal.objects.create(
                        diet=diet,
                        food_name=name,
                        calories=int(calories)
                    )
            messages.success(request, 'Dieta criada com sucesso!')
            return redirect('diet:diet_page')
    else:
        form = DietForm()
    
    return render(request, 'add_diet.html', {'form': form})

@login_required
def edit_diet(request, diet_id):
    dieta = get_object_or_404(DietPersist, id=diet_id, user=request.user)

    if request.method == 'POST':
        form = DietForm(request.POST, instance=dieta)

        # Se clicou no botão "Adicionar prato", apenas adiciona um formulário vazio
        if 'add' in request.POST:
            formset = DietMealFormSet(request.POST, instance=dieta, extra=1)
        else:
            formset = DietMealFormSet(request.POST, instance=dieta)
            # Se clicou em "Salvar"
            if form.is_valid() and formset.is_valid():
                form.save()
                formset.save()
                messages.success(request, 'Dieta atualizada com sucesso!')
                return redirect('diet:diet_detail', diet_id=dieta.id)
    else:
        form = DietForm(instance=dieta)
        formset = DietMealFormSet(instance=dieta)

    return render(request, 'edit_diet.html', {
        'form': form,
        'formset': formset,
        'dieta': dieta
    })

    
@login_required
def delete_diet(request, diet_id):
    dieta = get_object_or_404(DietPersist, id=diet_id, user=request.user)
    
    if request.method == 'POST':
        # 1. Se o usuário confirmou (clicou no botão "Excluir" dentro do form)
        dieta.delete()
        messages.success(request, 'Dieta excluída com sucesso.')
        # 2. Volta para a lista de dietas
        return redirect('diet:diet_page') 
    
    # 1. Se for GET, apenas mostra a página de confirmação
    return render(request, 'delete_diet_confirm.html', {'dieta': dieta})

