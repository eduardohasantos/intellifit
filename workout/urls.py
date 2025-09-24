from django.urls import path
from . import views

urlpatterns = [
    path('', views.workout, name="workout"),
    path('add/', views.add_workout, name="add_workout"),
    path('add/exercise/', views.add_exercise, name="add_exercise"),
    path('<int:workout_id>/', views.workout_detail, name="workout_detail"),
    path('<int:workout_id>/edit/', views.edit_workout, name="edit_workout"),
    path('<int:workout_id>/delete/', views.delete_workout, name="delete_workout"),
]