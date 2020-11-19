from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Evento
# Create your views here.


def index(request):
    lista_evn_rct = Evento.objects.order_by('-inicio')[:5]
    context = {'lista_evn_rct':lista_evn_rct}
    return render(request, 'eventos/index.html', context)


def detail(request, evento_nome):
    evento = get_object_or_404(Evento, nome=evento_nome)
    return render(request, 'eventos/detail.html', {'evento': evento})


def inscricao(request, evento_nome):
    return HttpResponse('Você está se inscrevendo no evento %s' %evento_nome)
