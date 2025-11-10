from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('create/', views.note_create, name='note_create'),
    path('<int:pk>/', views.note_detail, name='note_detail'),   
    path('<int:pk>/edit', views.edit_notes, name='edit_notes'),
    path('<int:pk>/delete', views.delete_notes, name='delete_notes')
]

