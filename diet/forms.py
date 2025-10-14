from django import forms
from .models import DietPersist, DaysOfTheWeek

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
