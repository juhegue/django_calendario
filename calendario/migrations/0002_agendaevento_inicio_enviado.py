# Generated by Django 3.2.16 on 2023-09-17 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendaevento',
            name='inicio_enviado',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Inicio enviado'),
        ),
    ]
