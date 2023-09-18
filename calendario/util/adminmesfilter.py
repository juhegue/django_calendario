# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime
from monthdelta import monthdelta
from calendar import monthrange
import logging

from django.contrib.admin import SimpleListFilter
from django.utils import timezone


logger = logging.getLogger(__name__)


class MesFilter(SimpleListFilter):
    """
    Filtro por meses en admin

    Se tiene que definir 'field_date_filter' con el campo fecha a filtrar,
    este puede ser un str con formato 'yyyymmdd' o un datetime

    """
    title = ''
    parameter_name = 'mes'

    valor_defecto = None
    modelo = None
    campo_fecha = None
    orden = None
    MESES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
             'Noviembre', 'Diciembre']

    def lookups(self, request, modeladmin):
        self.modelo = modeladmin.model
        self.campo_fecha = modeladmin.field_date_filter
        self.title = modeladmin.field_date_filter.split('__')[-1].replace('_', ' ')
        self.orden = modeladmin.field_order_filter if hasattr(modeladmin, 'field_order_filter') else None

        try:
            param = self.used_parameters[self.parameter_name]
            year = int(param[0:4])
            mes = int(param[4:6])
            inicial = datetime(year, mes, 1)
        except:
            inicial = self.get_ultimo()

        resul = list()
        for m in range(-6, 6):
            f = inicial + monthdelta(m)
            key = f.year * 100 + f.month
            resul.append((key, '%s-%02d %s' % (f.year, f.month, self.MESES[f.month - 1])))

        return resul[::-1]

    def queryset(self, request, queryset):
        if self.value():
            try:
                dfecha = self.value() + '01'
                year = int(dfecha[0:4])
                mes = int(dfecha[4:6])
                hfecha = datetime(year, mes, monthrange(year, mes)[1], 23, 59, 59).strftime('%Y%m%d')
                filtro = {'%s__range' % self.campo_fecha: (dfecha, hfecha)}
                query = queryset.filter(**filtro)
                if self.orden:
                    return query.order_by(self.orden)
                return query
            except:
                try:
                    fecha = self.value()
                    year = int(fecha[0:4])
                    mes = int(fecha[4:6])
                    dfecha = datetime(year, mes, 1)
                    hfecha = datetime(year, mes, monthrange(year, mes)[1], 23, 59, 59)
                    filtro = {'%s__range' % self.campo_fecha: (dfecha, hfecha)}
                    query = queryset.filter(**filtro)
                    if self.orden:
                        return query.order_by(self.orden)
                    return query
                except:
                    pass

        return queryset

    def get_ultimo(self):
        ultimo = self.modelo.objects.last()
        if ultimo:
            fecha = self._getitem(ultimo, self.campo_fecha)
            try:
                year = fecha.year
                mes = fecha.month
            except:
                year = int(fecha[0:4])
                mes = int(fecha[4:6])

            try:
                fecha = datetime(year, mes, 1)
            except:
                fecha = timezone.now()
        else:
            fecha = timezone.now()

        return fecha

    @staticmethod
    def _getitem(query, name):
        for attr in name.split('__'):
            query = getattr(query, attr, None)
        return query
