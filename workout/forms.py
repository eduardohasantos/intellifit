from django import forms
from .models import Workout, WorkoutExercise, Exercise

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'description']
        labels = {
            'name': 'Nome do treino',
            'description': 'Descrição (opcional)',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do treino'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição do treino (opcional)', 'rows': 3}),
        }

class WorkoutExerciseForm(forms.ModelForm):
    exercise_name = forms.CharField(
        label='Nome do exercício',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do exercício', 'autocomplete': 'off'})
    )

    class Meta:
        model = WorkoutExercise
        fields = ['exercise_name', 'sets', 'reps']
        labels = {
            'sets': 'Séries',
            'reps': 'Repetições',
        }
        widgets = {
            'sets': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'reps': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('exercise', None)
