from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
import json
from users.models import Participante, User, Organizador, PerguntaExtra
from django.utils import timezone
from eventos.models import Evento
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm

class ParticipanteInscricaoForm(BSModalForm):    
    def __init__(self, *args, **kwargs):
        eventos = Evento.objects.filter(inicio__gt=timezone.now()).order_by('inicio')
        request = kwargs.pop("request")
        super(ParticipanteInscricaoForm, self).__init__(*args,**kwargs)
        for evento in eventos:
            if evento.inscritos.filter(user=request.user):
                jaI = True
            else:
                jaI = False
            self.fields['evento%s' % evento.pk] = forms.BooleanField(label=evento.nome, required=False, initial=jaI)


class ParticipanteCreationForm(UserCreationForm):
    faculdade = forms.CharField(max_length=100)
    nascimento = forms.DateField()
    curso = forms.CharField(max_length=50)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    def __init__(self, *args, **kwargs):
        extra = PerguntaExtra.objects.all()
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for i, question in enumerate(extra):
            self.fields['extra%s' % i] = forms.CharField(label=question)

    @transaction.atomic
    def save(self):
        extra = PerguntaExtra.objects.all()
        user = super().save(commit=False)
        user.is_participant = True
        user.save()
        data = {}
        for i, question in enumerate(extra):
            data[question.texto] = self.cleaned_data.get('extra%s' % i)
        participante = Participante.objects.create(user=user, faculdade=self.cleaned_data.get('faculdade'), nascimento=self.cleaned_data.get('nascimento'), curso=self.cleaned_data.get('curso'), extraQuestions=data)
        return user

class OrganizadorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email']
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_organizador = True
        user.save()
        organizador = Organizador.objects.create(user=user)
        return user

class ParticipanteModalForm(forms.ModelForm):
    class Meta:
        model = Participante
        exclude = ('user','extraQuestions')
    def __init__(self, *args, **kwargs):
        extra = PerguntaExtra.objects.all()
        part = kwargs.pop("instance")
        super(forms.ModelForm, self).__init__(*args, instance=part)
        for i, question in enumerate(extra):
            try:
                self.fields['extra%s' % i] = forms.CharField(label=question, initial=part.extraQuestions[str(question)])
            except:
                self.fields['extra%s' % i] = forms.CharField(label=question)
            
    def save(self):
        extra = PerguntaExtra.objects.all()
        part = super().save(commit=False)
        data = {}
        for i, question in enumerate(extra):
            data[question.texto] = self.cleaned_data.get('extra%s' % i)
        part.extraQuestions = data
        part.save()
        return part

class UserModalForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

class OrgModalForm(BSModalModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

class PerguntaModelForm(BSModalModelForm):
    class Meta:
        model = PerguntaExtra
        fields = '__all__'