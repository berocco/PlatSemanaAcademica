# Generated by Django 3.1.3 on 2020-11-18 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evento',
            old_name='empresa',
            new_name='CA',
        ),
        migrations.AlterField(
            model_name='evento',
            name='fim',
            field=models.DateTimeField(verbose_name='fim do evento'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='inicio',
            field=models.DateTimeField(verbose_name='início do evento'),
        ),
    ]