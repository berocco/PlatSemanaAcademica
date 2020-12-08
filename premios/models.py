from django.db import models
from users.models import Participante

class Premio(models.Model):
    meta = models.IntegerField(verbose_name='Meta de presenças para ganhar')
    premio = models.CharField(max_length=100)

    ganhadores = models.ManyToManyField(Participante, related_name='ganhou_premio', blank=True)
