# users/forms.py

from django import forms
from django.contrib.auth.models import User

class UserEditForm(forms.ModelForm):
    # O campo 'email' é obrigatório por padrão, vamos garantir isso.
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        # Defina os campos que o usuário pode editar.
        # Você pode adicionar 'first_name', 'last_name', etc.
        fields = ('username', 'email')