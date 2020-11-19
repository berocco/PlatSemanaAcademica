from django.urls import path
from . import views

app_name = 'eventos'
urlpatterns = [
    path('', views.index, name='index'),
    path('novo/', views.novo, name='novo'),
    path('ver/<str:evento_nome>/', views.detail, name='detail'),
    path('inscricao/<str:evento_nome>/', views.inscricao, name='inscricao'),
]