from django.utils import timezone
from datetime import timedelta
from .models import Evento

def CurrentEventMiddleware(get_response):
    def middleware(request):
        dt =  timedelta(minutes=30)
        now = timezone.now()
        Evento.objects.filter(abertoParticipar=True).update(abertoParticipar=False)
        sbo = Evento.objects.filter(inicio__lte=now+dt, inicio__gte=now-dt)
        if sbo:
            sbo.update(abertoParticipar=True)
        Evento.objects.filter(abertoFeedback=True).update(abertoFeedback=False)

        sbf = Evento.objects.filter(fim__lte=now+dt, fim__gte=now-dt)
        if sbf:            
            sbf.update(abertoFeedback=True)
        response = get_response(request)
        return response
    return middleware