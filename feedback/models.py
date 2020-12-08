from django.db import models
from users.models import Participante
from eventos.models import Evento

CHOICES = [(0, '0 (Nada)'), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, '10 (Muito)')]

class Feedback(models.Model):
    evento = models.ForeignKey(Evento, related_name='feedbacks', on_delete=models.CASCADE)
    autor =  models.ForeignKey(Participante, related_name='feedbacks', on_delete=models.CASCADE)

    expectativa = models.IntegerField(verbose_name="Quanto o evento atendeu às suas expectativas?",
                                    help_text='Sendo 0 = "Não gostei nada" e 10 = "Amei tudo"', 
                                    choices=CHOICES)
    tema = models.IntegerField(verbose_name="Quanto você gostou do tema do evento?",
                                    help_text='Sendo 0 = "Não gostei nada" e 10 = "Amei tudo"', 
                                    choices=CHOICES)
    organização = models.IntegerField(verbose_name="Quanto você gostou da organização do evento?",
                                    help_text='Sendo 0 = "Não gostei nada" e 10 = "Amei tudo"', 
                                    choices=CHOICES)
    comentários = models.TextField(verbose_name="Comentários gerais sobre o evento:", blank=True, null=True)
    extraQuestions = models.JSONField(null=True)

    class Meta:
        unique_together = (("evento", "autor"),)

class PerguntaFeedback(models.Model):
    evento = models.ForeignKey(Evento, related_name='perguntas_feedback', on_delete=models.CASCADE)
    texto = models.CharField(max_length=250)
    def __str__(self):
        return self.texto