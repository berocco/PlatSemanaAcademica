"""PSA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, auth
from django.urls import path
from django.conf.urls import include
from users import views as user_views
from premios import views as premios_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('conta/', login_required(user_views.minhaconta), name='my_account'),
    path('conta/editar', login_required(user_views.self_edit_profile), name='selfedit'),
    path('conta/', include('django.contrib.auth.urls')),

    path('admin/', admin.site.urls),

    path('', login_required(user_views.dashboard), name="dashboard"),

    path("cadastro/", user_views.ParticipanteRegister.as_view(), name='register'),
    path("cadastro/organizador/", login_required(user_views.OrganizadorRegister.as_view()), name='registerOrg'),
    path('cadastro/perguntas/', login_required(user_views.OrgPerguntasInscricao), name='perguntasInscricao'),
    path('cadastro/perguntas/criar', login_required(user_views.PerguntaCreateView.as_view()), name='createInscQuestion'),
    path('cadastro/perguntas/editar/<int:pk>', login_required(user_views.PerguntaUpdateView.as_view()), name='editInscQuestion'),
    path('cadastro/perguntas/deletar/<int:pk>', login_required(user_views.PerguntaDeleteView.as_view()), name='deleteInscQuestion'),



    path('feedbacks/', include('feedback.urls')),
    path('eventos/', include('eventos.urls')),

    path('editatinscricao/',  login_required(user_views.editInsc), name='editInsc'),
    path('usuario/deletar/<int:pk>', login_required(user_views.ParticipanteDeleteView.as_view()), name='deleteUser'),
    path('usuario/editar/<int:pk>', login_required(user_views.edit_profile), name='editUser'),
    path('usuario/detalhes/<int:pk>', login_required(user_views.ParticipanteReadView.as_view()), name='detalhesUser'),
    path('orgazador/editar/<int:pk>', login_required(user_views.UserUpdateView.as_view()), name='editOrg'),

    path('pessoas/', login_required(user_views.orgPessoas), name='pesoasOrg'),

    path('premios/', login_required(premios_views.mainPremios), name='premiosMain'),
    path('premios/criar/', login_required(premios_views.PremioCreateView.as_view()), name='createPremio'),
    path('premios/editar/<int:pk>', login_required(premios_views.PremioUpdateView.as_view()), name='updatePremio'),
    path('premios/deletar/<int:pk>', login_required(premios_views.PremioDeleteView.as_view()), name='deletePremio')
]
