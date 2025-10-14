from django import forms
from .models import DaysOfTheWeek, DietPersist


class dietForm:
    class meta:
        model = DietPersist
        fields = ['dietTitle', 'dietDescription']
        
        labels = {
            'name' : 'nome da dieta',
            'description' : 'descrição da dieta'
        }
        
        #widgets = entender que campo é esse!!
    