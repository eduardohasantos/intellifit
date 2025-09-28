# Arquivo: progress/urls.py

from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    # A URL principal /progress/ vai para a nossa view principal
    path('', views.progress_page, name='progress_page'),
    
    # A URL /progress/edit/1/ (por exemplo) vai para a view de edição
    path('edit/<int:entry_id>/', views.edit_progress_page, name='edit_progress'),
]