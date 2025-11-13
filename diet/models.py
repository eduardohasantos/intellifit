from django.db import models

class DietPersist(models.Model):
    dietTitle = models.CharField(max_length=60)
    dietDescription = models.TextField(blank=False, null=True)
    dietData = models.DateField(auto_now_add=True)
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='dietas',
        # null=True,
        # blank=True,
    )

    def __str__(self):
        return self.dietTitle

class DietMeal(models.Model):
    diet = models.ForeignKey(DietPersist, on_delete=models.CASCADE, related_name='meals')
    food_name = models.CharField(max_length=100)
    calories = models.IntegerField()


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
