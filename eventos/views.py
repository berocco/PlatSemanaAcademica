from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Evento
from .forms import EventoForm
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView, BSModalReadView
import datetime
from itertools import groupby
from django.utils import timezone
import pytz
from users.models import Participante
from premios.models import Premio
from users.views import isOrgMixin, org_check, part_check
from django.contrib.auth.decorators import user_passes_test

def detail(request, evento_nome):
    evento = get_object_or_404(Evento, nome=evento_nome)
    return render(request, './eventos/detail.html', {'evento': evento})

class EventCreateView(isOrgMixin, BSModalCreateView):
    template_name = './eventos/createEvent.html'
    form_class = EventoForm
    success_message = 'Success: Event was created.'
    success_url = reverse_lazy('eventos:index')

class EventEditView(isOrgMixin, BSModalUpdateView):
    model = Evento
    template_name = './eventos/updateEvent.html'
    form_class = EventoForm
    success_message = 'Success: Event was updated.'
    success_url = reverse_lazy('eventos:index')

class EventDeleteView(isOrgMixin, BSModalDeleteView):
    model = Evento
    template_name = './eventos/deleteEvent.html'
    success_message = 'Success: Event was deleted.'
    success_url = reverse_lazy('eventos:index')

class EventReadView(isOrgMixin, BSModalReadView):
    model = Evento
    template_name = 'eventos/detailEvent.html'

def datetime_range(start, end, delta):
    current = start
    while current <= end:
        yield current
        current += delta
def extract_date(entity):
    return entity.inicio.date()
def ScheduleView(request):
    #adicionar botao condicional ao user
    context = {}
    try:
        eventos = Evento.objects.all()
        evStart = eventos.order_by('inicio__hour', 'inicio__minute').first().inicio
        evFinish = eventos.order_by('fim__hour', 'fim__minute').last().fim
        eventosOrdered = eventos.order_by('inicio')
        roundedStart = evStart - datetime.timedelta(minutes=+180 + evStart.minute % 30)
        if evFinish.minute == 0 or evFinish.minute == 30:
            roundedEnd = evFinish + datetime.timedelta(minutes=-180)
        else:
            roundedEnd = evFinish + datetime.timedelta(minutes=-150 - (evFinish.minute % 30))
        times = [dt.strftime('%H:%M') for dt in datetime_range(roundedStart.replace(day=1, month=1), roundedEnd.replace(day=1, month=1), datetime.timedelta(minutes=30))]
        dates = [dt.strftime('%d/%m') for dt in datetime_range(eventosOrdered.first().inicio, eventosOrdered.last().inicio, datetime.timedelta(days=1))]
        list_of_lists = {t.strftime('%d/%m'):list(g) for t, g in groupby(eventosOrdered, key=extract_date)}
        context = {'times':times, 'dates':dates, 'eventos':list_of_lists}
    except:
        context = {'times':None, 'dates':None, 'eventos':None}
    return render(request, './eventos/schedule.html', context)

@user_passes_test(org_check, login_url='dashboard', redirect_field_name=None)
def orgEventos(request):
    eventos = Evento.objects.all().order_by('inicio')
    context = {'eventos':eventos}
    return render(request, "eventos/org.html", context)

@user_passes_test(part_check, login_url='dashboard', redirect_field_name=None)
def currentEvent(request, pk):
    eve = Evento.objects.get(pk=pk)
    if eve.inicio <= timezone.now() + datetime.timedelta(minutes=30) and eve.fim >= timezone.now() - datetime.timedelta(minutes=30):
        u = Participante.objects.get(pk=request.user.pk)
        if eve.abertoParticipar or eve.presentes.filter(pk = u.pk).exists():
            eve.presentes.add(u)
            context = {'evento':eve}
            return render(request, "eventos/currentEvent.html", context)
        else:
            return redirect('dashboard')
    else:
        return redirect('dashboard')


@user_passes_test(part_check, login_url='dashboard', redirect_field_name=None)
def agoraRedi(request):
    try:
        u = Participante.objects.get(pk=request.user.pk)
        eventoAberto = Evento.objects.get(abertoParticipar=True)
        eventoAberto.presentes.add(u)
        pre = u.presente_em.all().count()
        for p in Premio.objects.all():
            if p.meta<=pre:
                p.ganhadores.add(u)
        return HttpResponseRedirect('../agora/'+str(eventoAberto.pk))   
    except:
        return redirect('dashboard')








