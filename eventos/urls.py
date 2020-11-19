from django.urls import path
from . import views

app_name = 'eventos'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:evento_nome>/', views.detail, name='detail'),
    path('<str:evento_nome>/inscricao/', views.inscricao, name='inscricao'),
]