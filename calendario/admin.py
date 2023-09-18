# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.conf.locale.es import formats as es_fotmats

from .models import AgendaEvento
from .models import AgendaEventoColor
from .models import Fcm

from .util.notificacionfcm import NotificacionFcm
from .util.adminmesfilter import MesFilter


es_fotmats.DATETIME_FORMAT = 'd/m/y H:i'
es_fotmats.DATE_FORMAT = 'd/m/y'


class Color:
    def _color(self, obj):
        return mark_safe(f'<div class="color" style="background-color:{obj.color};"></div>')

    class Media:
        css = {
             'all': ('calendario/css/admin.css',)
        }


def notifica_fcm_demo(modeladmin, request, queryset):
    for q in queryset:
        n = NotificacionFcm(q.user)
        n.demo()


class AgendaEventoAdmin(admin.ModelAdmin, Color):
    list_display = ('id', 'usuario', '_color', 'dia_completo', 'aviso_email', 'aviso_movil', 'inicio', 'fin',
                    'email_enviado','movil_enviado', 'inicio_enviado', 'titulo')
    ordering = ('usuario', '-inicio')
    search_fields = ('usuario', 'color', 'inicio', 'fin', 'titulo')
    field_date_filter = 'creado'
    list_filter = ['usuario', MesFilter]


admin.site.register(AgendaEvento, AgendaEventoAdmin)


class AgendaEventoColorAdmin(admin.ModelAdmin, Color):
    list_display = ('usuario', '_color')
    ordering = ('usuario', 'color')
    search_fields = ('usuario', 'color')
    field_date_filter = 'creado'
    list_filter = ['usuario', MesFilter]


admin.site.register(AgendaEventoColor, AgendaEventoColorAdmin)


class FcmAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')
    actions = [notifica_fcm_demo]


admin.site.register(Fcm, FcmAdmin)

