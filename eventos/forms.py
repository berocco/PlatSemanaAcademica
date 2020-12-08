from django import forms
from .models import Evento
from users.models import Participante
from bootstrap_modal_forms.forms import BSModalModelForm

class EventoForm(BSModalModelForm):
    class Meta:
        model = Evento
        exclude = ['inscritos', 'presentes', 'abertoParticipar', 'abertoFeedback']
