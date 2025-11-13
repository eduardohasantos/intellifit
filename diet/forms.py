from django import forms
from .models import DietPersist, DietMeal
from django.forms import inlineformset_factory

class DietForm(forms.ModelForm):
    class Meta:
        model = DietPersist
        fields = ['dietTitle', 'dietDescription']
        labels = {
            'dietTitle': 'Título da dieta',
            'dietDescription': 'Descrição da dieta',
        }
        widgets = {
            'dietTitle': forms.TextInput(attrs={'placeholder': 'Ex: Dieta para ganho de massa'}),
            'dietDescription': forms.Textarea(attrs={'placeholder': 'Descreva o objetivo ou detalhes da dieta'}),
        }

class DietMealForm(forms.ModelForm):
    class Meta:
        model = DietMeal
        fields = ['food_name', 'calories']
        labels = {
            'food_name': 'Alimento',
            'calories': 'Calorias (kcal)',
        }
        widgets = {
            'food_name': forms.TextInput(attrs={'placeholder': 'Ex: Peito de frango'}),
            'calories': forms.NumberInput(attrs={'placeholder': 'Ex: 200'}),
        }

DietMealFormSet = inlineformset_factory(
    DietPersist, DietMeal,
    form=DietMealForm,
    extra=1,
    can_delete=True
)
