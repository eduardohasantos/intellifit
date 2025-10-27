from django import forms
from .models import DietPersist, DaysOfTheWeek,DietMeal
from django.forms import inlineformset_factory

# O ponto crucial: A classe do formulário deve herdar de forms.ModelForm
class DietForm(forms.ModelForm):
    # Definindo a Meta Classe (Metadata) para o formulário
    class Meta:
        # 1. Qual modelo este formulário deve usar?
        model = DietPersist
        
        # 2. Quais campos do modelo devem ser incluídos no formulário?
        fields = ['dietTitle', 'dietDescription']
        
        # 3. Personalizar rótulos (Labels) que aparecerão no formulário
        labels = {
            # Atenção: as chaves (keys) aqui devem ser os nomes EXATOS dos campos do modelo
            'dietTitle': 'Nome da Dieta',
            'dietDescription': 'Descrição/Observações',
        }
        
        # 4. Personalizar os widgets (tipo de input, placeholders, classes CSS)
        widgets = {
            'dietTitle': forms.TextInput(attrs={'placeholder': 'Ex: Dieta para Ganho de Massa'}),
            'dietDescription': forms.Textarea(attrs={'placeholder': 'Detalhe o objetivo ou outras informações relevantes...', 'rows': 4}),
        }



class DietMealForm(forms.ModelForm):
    class Meta:
        model = DietMeal
        # Campos do "Prato"
        fields = ['food_name', 'calories']
        widgets = {
            'food_name': forms.TextInput(attrs={'class': 'form-control'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# 1. Isso cria um "conjunto de formulários" para os pratos (DietMeal) que estão ligados à dieta (DietPersist).


DietMealFormSet = inlineformset_factory(
    DietPersist,  # Modelo Pai
    DietMeal,     # Modelo Filho
    form=DietMealForm,
    # 2. extra=0: Começa sem nenhum campo de prato em branco.
    extra=0,
    # 3. can_delete=True: Permite marcar pratos existentes para exclusão.
    can_delete=True,
)