from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Workout, WorkoutExercise, Exercise
def edit_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    exercises = WorkoutExercise.objects.filter(workout=workout).select_related('exercise').order_by('id')
    from .forms import WorkoutExerciseForm
    from .models import Exercise
    message = None
    if request.method == 'POST':
        # Remover exercício
        if 'remove_exercise' in request.POST:
            ex_id = request.POST.get('remove_exercise')
            WorkoutExercise.objects.filter(id=ex_id, workout=workout).delete()
            return HttpResponseRedirect(reverse('edit_workout', args=[workout.id]))
        # Adicionar novo exercício
        if 'add_exercise' in request.POST:
            ex_form = WorkoutExerciseForm(request.POST)
            if ex_form.is_valid():
                exercise_name = ex_form.cleaned_data['exercise_name']
                exercise_obj, _ = Exercise.objects.get_or_create(name=exercise_name)
                workout_exercise = ex_form.save(commit=False)
                workout_exercise.workout = workout
                workout_exercise.exercise = exercise_obj
                workout_exercise.save()
                return HttpResponseRedirect(reverse('edit_workout', args=[workout.id]))
            else:
                message = 'Erro ao adicionar exercício.'
        if 'save_workout' in request.POST:
            # Atualiza nome e descrição
            workout.name = request.POST.get('name', workout.name)
            workout.description = request.POST.get('description', workout.description)
            workout.save()
            # Atualiza exercícios
            for ex in exercises:
                sets = request.POST.get(f'sets_{ex.id}')
                reps = request.POST.get(f'reps_{ex.id}')
                if sets and reps:
                    ex.sets = sets
                    ex.reps = reps
                    ex.save()
            # Atualiza ordem
            order_list = request.POST.getlist('order')
            if order_list:
                for idx, ex_id in enumerate(order_list):
                    try:
                        ex = WorkoutExercise.objects.get(id=ex_id, workout=workout)
                        ex.order = idx + 1
                        ex.save()
                    except WorkoutExercise.DoesNotExist:
                        pass
            # Redireciona para página de detalhes do treino com popup de sucesso
            response = HttpResponseRedirect(reverse('workout_detail', args=[workout.id]))
            response.set_cookie('success_message', 'Alterações salvas', max_age=3, path=f'/workout/{workout.id}/')
            return response
    else:
        ex_form = WorkoutExerciseForm()
    # Buscar nomes de exercícios já cadastrados para autocomplete
    exercise_names = list(Exercise.objects.values_list('name', flat=True))
    return render(request, 'edit_workout.html', {
        'workout': workout,
        'exercises': exercises,
        'ex_form': ex_form,
        'exercise_names': exercise_names,
        'message': message
    })

def delete_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    if request.method == 'POST':
        workout.delete()
        return redirect('workout')
    return render(request, 'delete_workout.html', {'workout': workout})
from django.shortcuts import get_object_or_404

def workout_detail(request, workout_id):
    from .models import WorkoutExercise
    workout = get_object_or_404(Workout, id=workout_id)
    exercises = WorkoutExercise.objects.filter(workout=workout).select_related('exercise').order_by('id')
    return render(request, 'workout_detail.html', {
        'workout': workout,
        'exercises': exercises
    })

from django.shortcuts import render, redirect
from .models import Workout
from .forms import WorkoutForm, WorkoutExerciseForm

def workout(request):
    # Aqui você pode filtrar por usuário se houver relação
    workouts = Workout.objects.all()
    return render(request, 'workout.html', {'workouts': workouts})


def add_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save()
            # Redireciona para adicionar exercícios ao treino recém-criado
            request.session['workout_id'] = workout.id
            return redirect('add_exercise')
    else:
        form = WorkoutForm()
    return render(request, 'add_workout.html', {'form': form})


def add_exercise(request):
    from .models import Exercise
    workout_id = request.session.get('workout_id')
    if not workout_id:
        return redirect('workout')
    if request.method == 'POST':
        form = WorkoutExerciseForm(request.POST)
        if form.is_valid():
            exercise_name = form.cleaned_data['exercise_name']
            exercise_obj, _ = Exercise.objects.get_or_create(name=exercise_name)
            workout_exercise = form.save(commit=False)
            workout_exercise.workout_id = workout_id
            workout_exercise.exercise = exercise_obj
            workout_exercise.save()
            return redirect('add_exercise')
    else:
        form = WorkoutExerciseForm()
    # Buscar nomes de exercícios já cadastrados para autocomplete
    from django.http import JsonResponse
    exercise_names = list(Exercise.objects.values_list('name', flat=True))
    return render(request, 'add_exercise.html', {'form': form, 'exercise_names': exercise_names})
