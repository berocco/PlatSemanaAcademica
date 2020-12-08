from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'eventos'
urlpatterns = [
    path('criar/', login_required(views.EventCreateView.as_view()), name='novo'),
    path('detalhes/<str:evento_nome>/', views.detail, name='detail'),
    path('ver/<int:pk>/', login_required(views.EventReadView.as_view()), name='detail_event'),
    path('editar/<int:pk>/', login_required(views.EventEditView.as_view()), name='update_event'),
    path('deletar/<int:pk>', login_required(views.EventDeleteView.as_view()), name='delete_event'),
    path('', views.ScheduleView, name='index'),
    path('org/', login_required(views.orgEventos), name='evOrg'),

    path('agora/<int:pk>/', login_required(views.currentEvent), name='current'),
    path('agora/', login_required(views.agoraRedi), name='agora')
]