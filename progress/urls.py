from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('', views.progress_page, name='progress_page'),
    path('edit/<int:entry_id>/', views.edit_progress_page, name='edit_progress'),
    path('delete/<int:entry_id>/', views.delete_progress_page, name='delete_progress'),
]