
from .models import Premio
from bootstrap_modal_forms.forms import BSModalModelForm


class PremioModelForm(BSModalModelForm):
    class Meta:
        model = Premio
        exclude = ['ganhadores']