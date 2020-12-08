from django.db import models
from users.models import Participante
# Create your models here.


class Evento(models.Model):
    nome = models.CharField(max_length=200)
    inicio = models.DateTimeField(auto_now=False, auto_now_add=False)
    fim = models.DateTimeField(auto_now=False, auto_now_add=False)
    empresa = models.CharField(max_length=100)
    tema = models.CharField(max_length=100)
    descricao = models.CharField(max_length=1000)

    abertoParticipar = models.BooleanField(default=False)
    abertoFeedback = models.BooleanField(default=False)

    inscritos = models.ManyToManyField(Participante, related_name='inscrito_em', blank=True)
    presentes = models.ManyToManyField(Participante, related_name='presente_em', blank=True)

    def __str__(self):
        return self.nome
