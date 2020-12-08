from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import ParticipanteCreationForm,OrgModalForm, OrganizadorCreationForm, ParticipanteInscricaoForm, ParticipanteModalForm, UserModalForm, PerguntaModelForm
from users.models import User, Participante, Organizador, PerguntaExtra
from django.views.generic import CreateView
from eventos.models import Evento
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils import timezone
from bootstrap_modal_forms.generic import BSModalUpdateView, BSModalDeleteView, BSModalReadView, BSModalCreateView
from premios.models import Premio
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test

def org_check(user):
    return user.is_organizador

def part_check(user):
    return user.is_participant

class isOrgMixin(UserPassesTestMixin):
    def test_func(self):
        try:
            return self.request.user.is_organizador
        except:
            return False
            
def dashboard(request):
    if request.user.is_organizador:
        ativo = Evento.objects.filter(abertoParticipar=True)
        nextEventos = Evento.objects.filter(inicio__gt=timezone.now()).order_by('inicio')
        context = {'ativo':ativo, 'nextEventos':nextEventos}
        return render(request, "dashboardAdmin.html", context)
    elif Participante.objects.filter(pk=request.user.pk):
        u = Participante.objects.get(pk=request.user.pk)
        ativo = Evento.objects.filter(abertoParticipar=True)
        nextEventos = Evento.objects.filter(inicio__gt=timezone.now()).order_by('inicio')
        premios = Premio.objects.all().order_by('meta')
        presenca = u.presente_em.all().count()
        context = {'ativo':ativo, 'nextEventos':nextEventos, 'premios':premios, 'presenca':presenca}
        return render(request, "dashboard.html", context)
    

def minhaconta(request):
    try:
        u = Participante.objects.get(pk=request.user.pk)
    except:
        u = Organizador.objects.get(pk=request.user.pk)
    context = {'u':u}
    return render(request, "registration/account.html", context)

@user_passes_test(part_check, login_url='dashboard', redirect_field_name=None)
def self_edit_profile(request):
    pk = request.user.pk
    user = User.objects.get(pk=pk)
    part = Participante.objects.get(pk=pk)
    if request.method == 'POST':
        form = UserModalForm(request.POST, instance=user)
        participante_form = ParticipanteModalForm(request.POST, instance=part) 
        if form.is_valid() and participante_form.is_valid():
            user_form = form.save()
            custom_form = participante_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return HttpResponseRedirect('/conta/')
    else:
        form = UserModalForm(instance=user)
        profile_form = ParticipanteModalForm(instance=part)
        args = {'form':form, "Partform":profile_form}
        return render(request, 'users/editParticipante.html', args)

@user_passes_test(part_check, login_url='dashboard', redirect_field_name=None)
def editInsc(request):
    if request.method == 'POST':
        form = ParticipanteInscricaoForm(request.POST, request=request)
        if form.is_valid():
            resp = form.cleaned_data
            aut = Participante.objects.get(user=request.user)
            for i in resp:
                evento = Evento.objects.get(pk=i[6:])
                if resp[i] == True:
                    evento.inscritos.add(aut)
                else:
                    evento.inscritos.remove(aut)
            return HttpResponseRedirect('/')
    else:
        form = ParticipanteInscricaoForm(request=request)
    return render(request, 'formtemp.html', {'form': form})


class ParticipanteRegister(CreateView):
    model = User
    form_class = ParticipanteCreationForm
    template_name = '../templates/registration/register.html'
    
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'participante'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('dashboard')
    
class OrganizadorRegister(isOrgMixin, CreateView):
    model = User
    form_class = OrganizadorCreationForm
    template_name = '../templates/registration/register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'organizador'
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        user = form.save()
        return redirect('dashboard')

class ParticipanteDeleteView(isOrgMixin, BSModalDeleteView):
    model = User
    template_name = 'users/deleteUser.html'
    success_message = 'Success: Participante was deleted.'
    success_url = reverse_lazy('dashboardAdmin')

class ParticipanteReadView(isOrgMixin, BSModalReadView):
    model = Participante
    template_name = 'users/detalhesParticipante.html'

class UserUpdateView(isOrgMixin, BSModalUpdateView):
    model = User
    template_name = 'users/editUser.html'
    form_class = OrgModalForm
    success_message = 'Success: Organizer was updated.'
    success_url = reverse_lazy('pesoasOrg')

@user_passes_test(org_check, login_url='dashboard', redirect_field_name=None)
def edit_profile(request, pk):
    user = User.objects.get(pk=pk)
    part = Participante.objects.get(pk=pk)
    if request.method == 'POST':
        form = UserModalForm(request.POST, instance=user)
        participante_form = ParticipanteModalForm(request.POST, instance=part) 
        if form.is_valid() and participante_form.is_valid():
            user_form = form.save()
            custom_form = participante_form.save()
            custom_form.user = user_form
            custom_form.save()
            return HttpResponseRedirect(reverse('pesoasOrg'))
    else:
        form = UserModalForm(instance=user)
        profile_form = ParticipanteModalForm(instance=part)
        args = {'form':form, "Partform":profile_form}
        return render(request, 'users/editParticipante.html', args)

@user_passes_test(org_check, login_url='dashboard', redirect_field_name=None)
def orgPessoas(request):
    pessoas = Participante.objects.all().order_by('user__first_name')
    orgs = Organizador.objects.all().order_by('user__first_name')
    context = {'pats':pessoas, 'orgs':orgs}
    return render(request, "users/pessoas.html", context)

class PerguntaCreateView(isOrgMixin, BSModalCreateView):
    template_name = 'users/createPergunta.html'
    form_class = PerguntaModelForm
    success_message = 'Success: Pergunta was created.'
    success_url = reverse_lazy('perguntasInscricao')


class PerguntaUpdateView(isOrgMixin, BSModalUpdateView):
    model = PerguntaExtra
    template_name = 'users/editPergunta.html'
    form_class = PerguntaModelForm
    success_message = 'Success: Pergunta was updated.'
    success_url = reverse_lazy('perguntasInscricao')

class PerguntaDeleteView(isOrgMixin, BSModalDeleteView):
    model = PerguntaExtra
    template_name = 'users/deletePergunta.html'
    success_message = 'Success: Pergunta was deleted.'
    success_url = reverse_lazy('perguntasInscricao')

@user_passes_test(org_check, login_url='dashboard', redirect_field_name=None)
def OrgPerguntasInscricao(request):
    qs = PerguntaExtra.objects.all()
    context = {'qs':qs}
    return render(request, 'users/PergInsc.html', context)