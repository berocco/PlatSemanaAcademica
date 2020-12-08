from django import forms
from .models import Feedback, PerguntaFeedback
from eventos.models import Evento
from bootstrap_modal_forms.forms import BSModalModelForm

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ['evento', 'autor', 'extraQuestions']
    def __init__(self, *args, **kwargs):
        evento = Evento.objects.get(abertoFeedback=True)
        extra = PerguntaFeedback.objects.filter(evento=evento)
        super(FeedbackForm, self).__init__(*args, **kwargs)
        for i, question in enumerate(extra):
            self.fields['extra%s' % i] = forms.CharField(label=question)

class QuestaoModelForm(BSModalModelForm):
    class Meta:
        model = PerguntaFeedback
        fields = '__all__'