from django.db import models


class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField(default=3)
    reps = models.IntegerField(default=12)
    order = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.workout.name} - {self.exercise.name} ({self.sets}x{self.reps})"