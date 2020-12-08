from django.urls import reverse_lazy
from django.views import generic
from .forms import PremioModelForm
from django.shortcuts import redirect, render
from .models import Premio
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView
from users.views import isOrgMixin, org_check
from django.contrib.auth.decorators import user_passes_test

class PremioCreateView(isOrgMixin, BSModalCreateView):
    template_name = 'premios/criaPremio.html'
    form_class = PremioModelForm
    success_message = 'Success: Premio was created.'
    success_url = reverse_lazy('premiosMain')

class PremioUpdateView(isOrgMixin, BSModalUpdateView):
    model = Premio
    template_name = 'premios/editaPremio.html'
    form_class = PremioModelForm
    success_message = 'Success: Premio was updated.'
    success_url = reverse_lazy('premiosMain')

class PremioDeleteView(isOrgMixin, BSModalDeleteView):
    model = Premio
    template_name = 'premios/deletaPremio.html'
    success_message = 'Success: Premio was deleted.'
    success_url = reverse_lazy('premiosMain')

@user_passes_test(org_check, login_url='dashboard', redirect_field_name=None)
def mainPremios(request):
    ps = Premio.objects.all()
    context = {'ps':ps}
    return render(request, 'premios/OrgPremios.html', context)