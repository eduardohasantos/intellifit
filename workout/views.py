from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Workout, WorkoutExercise, Exercise
from .forms import WorkoutForm, WorkoutExerciseForm


def workout_list(request):
    """Lista os workouts do usuário autenticado"""
    if request.user.is_authenticated:
        workouts = Workout.objects.filter(user=request.user)
    else:
        workouts = Workout.objects.none()
    
    context = {'workouts': workouts}
    return render(request, 'workout.html', context)


def workout_detail(request, workout_id):
    """Exibe os detalhes de um workout específico (somente do dono)"""
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    exercises = WorkoutExercise.objects.filter(workout=workout).select_related('exercise').order_by('id')
    
    context = {
        'workout': workout,
        'exercises': exercises
    }
    return render(request, 'workout_detail.html', context)


def add_workout(request):
    """Cria um novo treino"""
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            if request.user.is_authenticated:
                workout.user = request.user
            workout.save()

            response = redirect('add_exercise', workout_id=workout.id)
            response.set_cookie('success_message', 'Treino criado com sucesso! Agora adicione os exercícios.', max_age=5)
            request.session['workout_id'] = workout.id
            return response
    else:
        form = WorkoutForm()
    
    return render(request, 'add_workout.html', {'form': form})


def add_exercise(request, workout_id):
    """Adiciona exercícios a um treino"""
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    exercise_names = Exercise.objects.values_list('name', flat=True)
    
    if request.method == 'POST':
        form = WorkoutExerciseForm(request.POST)
        if form.is_valid():
            exercise_name = form.cleaned_data['exercise_name']
            exercise_obj, _ = Exercise.objects.get_or_create(name=exercise_name)
            
            workout_exercise = form.save(commit=False)
            workout_exercise.workout = workout
            workout_exercise.exercise = exercise_obj
            workout_exercise.save()
            
            messages.success(request, f'Exercício "{exercise_name}" adicionado com sucesso!')
            return redirect('add_exercise', workout_id=workout.id)
    else:
        form = WorkoutExerciseForm()
    
    context = {
        'form': form,
        'exercise_names': exercise_names,
        'workout': workout
    }
    return render(request, 'add_exercise.html', context)


def edit_workout(request, workout_id):
    """Edita um treino existente"""
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    exercises = WorkoutExercise.objects.filter(workout=workout).select_related('exercise').order_by('id')
    exercise_names = Exercise.objects.values_list('name', flat=True)
    
    if request.method == 'POST':
        # Remover exercício
        if 'remove_exercise' in request.POST:
            ex_id = request.POST.get('remove_exercise')
            try:
                exercise_to_remove = WorkoutExercise.objects.get(id=ex_id, workout=workout)
                exercise_name = exercise_to_remove.exercise.name
                exercise_to_remove.delete()
                messages.success(request, f'Exercício "{exercise_name}" removido!')
            except WorkoutExercise.DoesNotExist:
                messages.error(request, 'Exercício não encontrado.')
            return redirect('edit_workout', workout_id=workout.id)
        
        # Adicionar exercício
        elif 'add_exercise' in request.POST:
            form = WorkoutExerciseForm(request.POST)
            if form.is_valid():
                exercise_name = form.cleaned_data['exercise_name']
                exercise_obj, _ = Exercise.objects.get_or_create(name=exercise_name)
                
                workout_exercise = form.save(commit=False)
                workout_exercise.workout = workout
                workout_exercise.exercise = exercise_obj
                workout_exercise.save()
                messages.success(request, f'Exercício "{exercise_name}" adicionado!')
            return redirect('edit_workout', workout_id=workout.id)
        
        # Salvar treino
        elif 'save_workout' in request.POST:
            workout.name = request.POST.get('name', workout.name)
            workout.description = request.POST.get('description', workout.description)
            workout.save()
            
            for exercise in exercises:
                sets = request.POST.get(f'sets_{exercise.id}')
                reps = request.POST.get(f'reps_{exercise.id}')
                rest_time = request.POST.get(f'rest_time_{exercise.id}')
                
                if sets and reps:
                    exercise.sets = sets
                    exercise.reps = reps
                    exercise.rest_time = rest_time or 0
                    exercise.save()
            
            messages.success(request, 'Treino atualizado com sucesso!')
            return redirect('workout_detail', workout_id=workout.id)
    
    else:
        form = WorkoutExerciseForm()
    
    context = {
        'workout': workout,
        'exercises': exercises,
        'form': form,
        'exercise_names': exercise_names
    }
    return render(request, 'edit_workout.html', context)


def delete_workout(request, workout_id):
    """Exclui um treino"""
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    
    if request.method == 'POST':
        workout_name = workout.name
        workout.delete()
        messages.success(request, f'Treino "{workout_name}" excluído com sucesso!')
        return redirect('workout_list')
    
    return render(request, 'delete_workout.html', {'workout': workout})


def finalize_workout(request):
    """Finaliza o cadastro do treino"""
    workout_id = request.session.get('workout_id')
    if workout_id:
        del request.session['workout_id']
        messages.success(request, 'Treino finalizado com sucesso!')
    return redirect('workout_list')



def exercise_autocomplete(request):
    """Retorna lista de exercícios para autocomplete"""
    if 'term' in request.GET:
        term = request.GET.get('term')
        exercises = Exercise.objects.filter(name__icontains=term).values_list('name', flat=True)
        return JsonResponse(list(exercises), safe=False)
    return JsonResponse([], safe=False)
