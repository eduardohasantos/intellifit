from django.urls import path
from . import views

app_name = 'diet'

urlPatterns=[
    path('create/', views.add_Diet, name="add workout"),
]
