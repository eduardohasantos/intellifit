from django.urls import path
from . import views

app_name = 'diet'

urlpatterns=[
    path('', views.add_Diet, name="add_Diet"),
    #path('create/', views.add_Diet, name="add_diet"),
    #path('/delete',)
    #path('/')
]
