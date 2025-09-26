from django.urls import path
from . import views

urlpatterns = [
    path('', views.workout_list, name='workout_list'),  # Alterado para workout_list
    path('add/', views.add_workout, name='add_workout'),
    path('<int:workout_id>/', views.workout_detail, name='workout_detail'),
    path('<int:workout_id>/edit/', views.edit_workout, name='edit_workout'),
    path('<int:workout_id>/delete/', views.delete_workout, name='delete_workout'),
    path('<int:workout_id>/add_exercise/', views.add_exercise, name='add_exercise'),
    path('finalize/', views.finalize_workout, name='finalize_workout'),
    path('api/exercises/', views.exercise_autocomplete, name='exercise_autocomplete'),
]