from django import forms
from .models import ProgressEntry

class ProgressEntryForm(forms.ModelForm):
    class Meta:
        model = ProgressEntry
        fields = ['weight', 'water_ml', 'calories']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Garante que o campo 'date' não seja tratado como obrigatório no form
        if 'date' in self.fields:
            self.fields['date'].required = False
