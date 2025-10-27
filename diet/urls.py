from django.urls import path
from . import views

app_name = 'diet'

urlpatterns=[
    path('', views.diet_page, name="diet_page"),
    path('create/', views.add_diet, name="add_diet"),
    path('detail/<int:diet_id>/', views.diet_detail, name="diet_detail"),
    path('<int:diet_id>/edit/', views.edit_diet, name='edit_diet'),
    path('<int:diet_id>/delete/', views.delete_diet, name='delete_diet'),
    #path('/delete',)
    #path('/')
]
