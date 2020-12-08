from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Feedback,PerguntaFeedback
from .forms import FeedbackForm, QuestaoModelForm
from eventos.models import Evento
from users.models import Participante
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView
from users.views import isOrgMixin, org_check
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(org_check, login_url='dashboard', redirect_field_name=None)
def allfeedbacks(request):
    fbs = Feedback.objects.all()
    context = {'fbs':fbs}
    return render(request, 'feedbacks/all.html', context)

def CreateFeedback(request):
    try:
        evento= Evento.objects.get(abertoFeedback=True)
        autor = Participante.objects.get(pk=request.user.pk)
    except:
        evento = None
        autor = None       
    if evento and autor:
        form = FeedbackForm(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.evento = evento
            obj.autor = autor
            extra = PerguntaFeedback.objects.filter(evento=evento)
            data = {}
            for i, question in enumerate(extra):
                data[question.texto] = form.cleaned_data.get('extra%s' % i)
            obj.extraQuestions = data
            obj.save()
            return HttpResponseRedirect('/')
        context = {'form' : form, 'evento':evento}
        return render(request, "feedbacks/forms.html", context)
    else:
        return HttpResponseRedirect('/')


class QuestaoCreateView(isOrgMixin, BSModalCreateView):
    template_name = 'feedbacks/createQuestion.html'
    form_class = QuestaoModelForm
    success_message = 'Success: Question was created.'
    success_url = reverse_lazy('feedbackQuestions')
    
class QuestaoUpdateView(isOrgMixin, BSModalUpdateView):
    model = PerguntaFeedback
    template_name = 'feedbacks/editQuestion.html'
    form_class = QuestaoModelForm
    success_message = 'Success: Question was updated.'
    success_url = reverse_lazy('feedbackQuestions')

class QuestaoDeleteView(isOrgMixin, BSModalDeleteView):
    model = PerguntaFeedback
    template_name = 'feedbacks/deleteQuestion.html'
    success_message = 'Success: Question was deleted.'
    success_url = reverse_lazy('feedbackQuestions')

@user_passes_test(org_check, login_url='dashboard', redirect_field_name=None)
def questionsAll(request):
    qs = PerguntaFeedback.objects.all()
    context = {'qs':qs}
    return render(request, 'feedbacks/OrgQuestions.html', context)

