from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/',  views.login, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.logout_view, name='logout'), 
    path('edit_account/', views.edit_account, name='edit_account'), 
    path('delete_account/', views.delete_account, name='delete_account'), 
]
