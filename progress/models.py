from django.db import models
from django.contrib.auth.models import User

# Criamos uma "tabela" no banco de dados para guardar os registros de progresso
class ProgressEntry(models.Model):
    # Vinculamos cada registro a um usuário específico. Se o usuário for deletado, seus registros também serão.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # A data em que o registro foi criado. É preenchida automaticamente.
    date = models.DateField(auto_now_add=True)
    
    # Usamos DecimalField para peso para garantir a precisão (ex: 80.5 kg)
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Peso (kg)")
    
    # Usamos IntegerField para valores inteiros como ML e calorias
    water_ml = models.IntegerField(verbose_name="Água (ml)")
    calories = models.IntegerField(verbose_name="Calorias (kcal)")

    def __str__(self):
        return f"Registro de {self.user.username} em {self.date}"
