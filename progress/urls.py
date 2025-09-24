from django.urls import path
from . import views

# Define o "sobrenome" (namespace) para as URLs deste app,
# permitindo que usemos {% url 'progress:...' %} nos templates.
app_name = 'progress'

urlpatterns = [
    # Rota para a página inicial do app "progress" (ex: /progress/)
    path('', views.progress_home, name='progress_home'),
    
    # Rota que você tinha para o dashboard dentro de progresso (ex: /progress/dashboard/)
    path('dashboard/', views.dashboard, name='progress_dashboard'),
    
    # A nova rota que criamos para a página "progress.html" (ex: /progress/progress/)
    path('progress/', views.progress_page, name='progress_page'),
]