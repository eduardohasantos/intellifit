from django.db import models

#Uma dieta pode estar em vários dias. Um dia só pode ter uma dieta, ou seja, a relação de dietas para semana é de 1 <-> N
#e a de dietas para dias é de 1 <-> 1.

class DietPersist(models.Model):
    dietTitle = models.CharField(max_length=20)
    dietDescription = models.TextField(blank=False, null=True)
    dietData = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.dietTitle


class DaysOfTheWeek(models.Model):
    nomeDia = models.CharField(
        max_length=20,
        choices=[
            ('seg', 'Segunda-feira'),
            ('ter', 'Terça-feira'),
            ('qua', 'Quarta-feira'),
            ('qui', 'Quinta-feira'),
            ('sex', 'Sexta-feira'),
            ('sab', 'Sábado'),
            ('dom', 'Domingo'),
        ]
    )

    dieta = models.ForeignKey(
        DietPersist,
        on_delete=models.CASCADE,
        related_name='dias'
    )

    def __str__(self):
        return self.get_nomeDia_display()
