# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# from django.contrib.auth.models import User
# se cambia por, ya que el user puede estar personalizad:
from django.contrib.auth import get_user_model
User = get_user_model()



class ActualizaMixin(models.Model):
    creado = models.DateTimeField(_('Creado'), editable=False)
    modificado = models.DateTimeField(_('Actualizado'))

    def save(self, *args, **kwargs):
        if not self.id:
            self.creado = timezone.now()
        self.modificado = timezone.now()
        return super(ActualizaMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class AgendaEventoColor(ActualizaMixin):
    usuario = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)
    color = models.CharField(verbose_name=_('Color'), max_length=7)

    class Meta:
        verbose_name = _('Agenda evento color')
        verbose_name_plural = _('Agenda evento colores')

    def __str__(self):
        return self.color


class AgendaEvento(ActualizaMixin):
    usuario = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)
    color = models.ForeignKey(AgendaEventoColor, verbose_name=_('Color'), on_delete=models.CASCADE)
    inicio = models.DateTimeField(verbose_name=_('Inicio evento'), db_index=True)
    fin = models.DateTimeField(verbose_name=_('Fin evento'), db_index=True)
    titulo = models.CharField(verbose_name=_('Título'), max_length=250)
    dia_completo = models.BooleanField(verbose_name=_('Todo el día'), default=True)
    aviso_email = models.BooleanField(verbose_name=_('Avisar con email'), default=False)
    aviso_movil = models.BooleanField(verbose_name=_('Avisar con móvil'), default=False)
    email_enviado = models.DateTimeField(verbose_name=_('Email enviado'), null=True, blank=True)
    movil_enviado = models.DateTimeField(verbose_name=_('Móvil enviado'), null=True, blank=True)
    inicio_enviado = models.DateTimeField(verbose_name=_('Inicio enviado'), null=True, blank=True)

    class Meta:
        verbose_name = _('Agenda evento')
        verbose_name_plural = _('Agenda eventos')

    def __str__(self):
        return self.titulo


# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model
class Fcm(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self):
        return self.token
