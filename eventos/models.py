from django.db import models

# Create your models here.


class Evento(models.Model):
    nome = models.CharField(max_length=200)
    CA = models.CharField(max_length=100)
    inicio = models.DateTimeField('início do evento')
    fim = models.DateTimeField('fim do evento')
    CA = models.CharField(max_length=100)
    tema = models.CharField(max_length=100)
    descricao = models.CharField(max_length=1000)
    def __str__(self):
        return self.nome
