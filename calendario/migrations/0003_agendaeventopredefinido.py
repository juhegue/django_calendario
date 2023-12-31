# Generated by Django 3.2.16 on 2023-09-19 21:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calendario', '0002_agendaevento_inicio_enviado'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgendaEventoPredefinido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(editable=False, verbose_name='Creado')),
                ('modificado', models.DateTimeField(verbose_name='Actualizado')),
                ('inicio', models.CharField(default='00:00', max_length=5, verbose_name='Hora inicio')),
                ('duracion', models.PositiveIntegerField(default=0, verbose_name='Minutos duración')),
                ('titulo', models.CharField(max_length=250, verbose_name='Título')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calendario.agendaeventocolor', verbose_name='Color')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Agenda evento predefinido',
                'verbose_name_plural': 'Agenda eventos predefinidos',
            },
        ),
    ]
