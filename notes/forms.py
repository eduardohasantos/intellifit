from django import forms
from .models import Note
from django.forms import Textarea

class editNotesForm(forms.ModelForm):

    class Meta:
        #Precisa ser model porque é a variável que será utilizada para representar um objeto note
        
        model = Note
        fields = ['title', 'content']
        
        labels = {
            'title' : 'Título da anotação',
            'content' : 'conteudo das anotações'
        }
        
        widgets = {
            'content': Textarea(attrs={'rows': 10}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)    