# -*- coding: utf-8 -*-

import json
import pytz
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.utils.timezone import make_aware
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from calendario.models import AgendaEvento, AgendaEventoColor, AgendaEventoPredefinido
from calendario.forms.eventoPredefinidoForm import EventoPedefinidoForm


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def get_color(request, color):
    if color.startswith('#'):
        color = color.upper()
        qcolor = AgendaEventoColor.objects.filter(usuario=request.user, color=color).first()
    else:
        qcolor = AgendaEventoColor.objects.filter(pk=color).first()

    if not qcolor:
        qcolor = AgendaEventoColor()
        qcolor.usuario = request.user
        qcolor.color = color
        qcolor.save()
    return qcolor


def defecto_agenda(request):
    if not AgendaEventoColor.objects.filter(usuario=request.user).exists():
        for color in ['#00ACAC', '#348FE2', '#F59C1A', '#FF5B57', '#2D353C', '#32A932', '#FV5597']:
            c = AgendaEventoColor()
            c.usuario = request.user
            c.color = color
            c.save()

    if not AgendaEventoPredefinido.objects.filter(usuario=request.user).exists():
        p = AgendaEventoPredefinido()
        p.usuario = request.user
        p.color = AgendaEventoColor.objects.get(usuario=request.user, color='#00ACAC')
        p.inicio = '00:00'
        p.duracion = 60 * 24
        p.titulo = 'Viaje'
        p.save()

        p = AgendaEventoPredefinido()
        p.usuario = request.user
        p.color = AgendaEventoColor.objects.get(usuario=request.user, color='#348FE2')
        p.inicio = '15:30'
        p.duracion = 60
        p.titulo = 'Reunión'
        p.save()


class CalendarioView(LoginRequiredMixin, TemplateView):
    template_name = 'calendario/calendario/calendario.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        defecto_agenda(self.request)
        eventos = list()
        for q in AgendaEventoPredefinido.objects.filter(usuario=self.request.user):
            eventos.append({
                'id': q.pk,
                'title': q.titulo,
                'inicio': q.inicio,
                'duracion': q.horas,
                'color': q.color.color,
            })
        context['eventos'] = eventos
        context['nav_activa'] = 'calendario'
        return context

    def get_colores(self, request):
        term = request.POST.get('term')
        page = int(request.POST.get('page'))

        limit = 100
        offset = (page - 1) * limit

        query = AgendaEventoColor.objects.filter(usuario=self.request.user)
        if term:
            query.filter(color__icontains=term)

        query = query.order_by('color')
        count = query.count()
        query = query[offset:limit + offset]

        data = list()
        for d in query:
            data.append({
                'id': d.pk,
                'text': d.color,
            })

        final = offset + limit
        mas = count > final

        resul = {
            'results': data,
            'pagination': {
                'more': mas
            }
        }
        return JsonResponse(resul, safe=False)

    def getall_colores(self):
        data = AgendaEventoColor.objects.filter(usuario=self.request.user).values_list('id', 'color')
        return JsonResponse({'err': False, 'param': list(data)}, safe=False)

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            param = request.POST.get('param')
            if param:
                if param == 'colores':   # llama select2
                    return self.get_colores(request)

                param = json.loads(param)
                accion = param.get('accion')
                data = param.get('data', dict())
                if accion == 'colores':
                    return self.getall_colores()
                elif accion == 'agendaEvento':
                    q = AgendaEvento.objects.filter(pk=param.get('id')).first()
                    data = {field.name: str(getattr(q, field.name)) for field in AgendaEvento._meta.fields}
                    return JsonResponse({'err': False, 'param': data}, safe=False)
                elif accion == 'borra':
                    AgendaEvento.objects.filter(pk=data.get('id')).delete()
                else:
                    if accion == 'receive':
                        inicio = datetime.strptime(data.get('start'), '%d/%m/%Y %H:%M')
                        inicio = pytz.timezone(settings.TIME_ZONE).localize(inicio).astimezone(pytz.timezone('UTC'))
                        pre = AgendaEventoPredefinido.objects.filter(pk=data.get('id')).first()
                        aevt = AgendaEvento()
                        aevt.usuario = request.user
                        aevt.color = pre.color
                        aevt.titulo = pre.titulo
                        aevt.dia_completo = True if pre.duracion % (60*24) == 0 and (pre.inicio == '00:00' or
                                                                                     pre.inicio == '0:00') else False
                        aevt.inicio = inicio
                        aevt.fin = aevt.inicio + timedelta(minutes=pre.duracion)
                        aevt.aviso_movil = pre.aviso_movil
                        aevt.aviso_email = pre.aviso_email
                    else:
                        if accion in ['resize', 'drop']:
                            aevt = AgendaEvento.objects.filter(pk=data.get('id')).first()
                        elif accion == 'actualiza':
                            color = data.get('color')
                            qcolor = get_color(request, color)
                            aevt = AgendaEvento.objects.filter(pk=data.get('id')).first()
                            if not aevt:
                                aevt = AgendaEvento()
                            aevt.usuario = request.user
                            aevt.color = qcolor
                            aevt.titulo = data.get('titulo')
                            aevt.dia_completo = True if data.get('completo', '') == 'on' else False
                            aevt.aviso_email = True if data.get('email') == 'on' else False
                            aevt.aviso_movil = True if data.get('movil') == 'on' else False

                        aevt.email_enviado = None
                        aevt.movil_enviado = None

                        inicio = datetime.strptime(data.get('inicio'), '%d/%m/%Y %H:%M')
                        if data.get('fin', ''):
                            try:
                                fin = datetime.strptime(data.get('fin'), '%d/%m/%Y %H:%M')
                            except:
                                fin = inicio
                        else:
                            fin = inicio
                            aevt.dia_completo = True

                        inicio = pytz.timezone(settings.TIME_ZONE).localize(inicio).astimezone(pytz.timezone('UTC'))
                        fin = pytz.timezone(settings.TIME_ZONE).localize(fin).astimezone(pytz.timezone('UTC'))

                        if inicio > fin:
                            aevt.inicio = fin
                            aevt.fin = inicio
                        elif inicio == fin:     # si son iguales añado un minuto
                            aevt.inicio = inicio
                            aevt.fin = fin + timedelta(minutes=1)
                        else:
                            aevt.inicio = inicio
                            aevt.fin = fin
                    aevt.save()
                return JsonResponse({'err': None, "param": {}})
            else:
                start = datetime.strptime(request.POST.get('start'), '%Y-%m-%dT%H:%M:%S.%fZ')
                end = datetime.strptime(request.POST.get('end'), '%Y-%m-%dT%H:%M:%S.%fZ')
                aware_start = make_aware(start)
                aware_end = make_aware(end)
                data = list()
                for q in AgendaEvento.objects.filter(usuario=self.request.user, inicio__lte=aware_end, fin__gte=aware_start):
                    inicio = timezone.localtime(q.inicio)
                    fin = timezone.localtime(q.fin)
                    start = inicio.strftime('%Y-%m-%d') if q.dia_completo else inicio.strftime('%Y-%m-%d %H:%M:%S')
                    end = fin.strftime('%Y-%m-%d') if q.dia_completo else fin.strftime('%Y-%m-%d %H:%M:%S')
                    data.append({
                            'id': q.pk,
                            'title': q.titulo,
                            'start': start,
                            'end': end,
                            'color': q.color.color,
                        })
                return JsonResponse({'data': data})


class RequiredEventoMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            pre = get_object_or_404(AgendaEventoPredefinido, pk=kwargs.get('pk'))
            if pre.usuario != request.user:
                messages.error(request, _('Sin permisos para esta acción.'))
                return redirect('logout_portal')
        return super().dispatch(request, *args, **kwargs)


class EventoPredefinidoListView(LoginRequiredMixin, ListView):
    model = AgendaEventoPredefinido
    template_name = 'calendario/predefinido/lista.html'

    def get_queryset(self):
        queryset = AgendaEventoPredefinido.objects.filter(usuario=self.request.user).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hidden"] = True
        return context


class EventoPredefinidoCreateView(LoginRequiredMixin, CreateView):
    model = AgendaEventoPredefinido
    template_name = 'calendario/predefinido/editar.html'
    form_class = EventoPedefinidoForm
    success_url = reverse_lazy('evento_predefinido_lista')
    success_message = _('Evento predefinido creado.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_view"] = True
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['object'] = None
        return kwargs

    def form_valid(self, form):
        f = form.save(commit=False)
        data = form.cleaned_data
        color = data.get('color')
        dias = data.get('dias') or 0
        horas = data.get('horas') or 0
        minutos = data.get('minutos') or 0

        f.color = get_color(self.request, color)
        f.usuario = self.request.user
        f.duracion = dias * 24 * 60 + horas * 60 + minutos
        f.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class EventoPredefinidoUpdateView(RequiredEventoMixin, UpdateView):
    model = AgendaEventoPredefinido
    template_name = 'calendario/predefinido/editar.html'
    form_class = EventoPedefinidoForm
    success_url = reverse_lazy('evento_predefinido_lista')
    success_message = _('Evento predefinido modificado.')

    def get_queryset(self):
        queryset = AgendaEventoPredefinido.objects.filter(usuario=self.request.user)
        return queryset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['object'] = self.object
        return kwargs

    def form_valid(self, form):
        f = form.save(commit=False)
        data = form.cleaned_data
        color = data.get('color')
        dias = data.get('dias') or 0
        horas = data.get('horas') or 0
        minutos = data.get('minutos') or 0

        f.color = get_color(self.request, color)
        f.duracion = dias * 24 * 60 + horas * 60 + minutos
        f.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class EventoPredefinidoDeleteView(RequiredEventoMixin, DeleteView):
    model = AgendaEventoPredefinido
    template_name = 'calendario/predefinido/eliminar.html'
    success_message = _('Evento prefefinido eliminado.')

    def get_queryset(self):
        queryset = AgendaEventoPredefinido.objects.filter(usuario=self.request.user)
        return queryset

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse('evento_predefinido_lista')
