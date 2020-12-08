from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager
from django.utils.translation import ugettext_lazy as _

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    is_participant = models.BooleanField(default=False)
    is_organizador = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.first_name+' '+self.last_name


class Participante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nascimento = models.DateField()
    faculdade = models.CharField(max_length=100)
    curso = models.CharField(max_length=50)

    extraQuestions = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.user.first_name+' '+self.user.last_name

class Organizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.first_name+' '+self.user.last_name
    
class PerguntaExtra(models.Model):
    texto = models.CharField(max_length=250)
    def __str__(self):
        return self.texto