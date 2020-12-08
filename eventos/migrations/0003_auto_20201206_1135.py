# Generated by Django 3.1.3 on 2020-12-06 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('eventos', '0002_evento_inscritos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='inscritos',
            field=models.ManyToManyField(blank=True, related_name='inscrito_em', to='users.Participante'),
        ),
    ]