# -*- coding: utf-8 -*-

import json
from django import forms
from django.urls import reverse
from calendario.models import AgendaEventoPredefinido
from django.utils.translation import gettext_lazy as _


class Custom(forms.ChoiceField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate(self, value):
        return value


class EventoPedefinidoForm(forms.ModelForm):
    data = forms.CharField(required=False, widget=forms.TextInput(attrs={"style": "display:none;"}))
    dias = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}),
                              label=_('Días'))
    minutos = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                 label=_('Minutos'))
    horas = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}),
                               label=_('Horas'))
    color = Custom(required=True, widget=forms.Select(attrs={'class': 'form-control color-select2',
                                                             'placeholder': _('Seleccione un color')}),
                   label=_('Color'),
                   help_text=_("Elija o añada un color en hexadecimal."))

    class Meta:
        model = AgendaEventoPredefinido
        fields = ('titulo', 'inicio', 'aviso_email', 'aviso_movil')
        labels = {
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'inicio': forms.TextInput(attrs={'class': 'form-control', 'aria-describedby': 'inicio'}),
            'aviso_email': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'aviso_movil': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
        }
        required = ('titulo', )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        object = kwargs.pop('object')
        super().__init__(*args, **kwargs)

        data_url = reverse('calendario')
        self.fields['color'].widget.attrs.update({'data-url': data_url})

        data = {
            'color': [[object.color.id, object.color.color]] if object else '',
        }
        self.fields['data'].initial = json.dumps(data)

        if object:
            minutos = object.duracion
            dias = int(minutos / 60 / 24)
            minutos -= dias * 60 * 24
            horas = int(minutos / 60)
            minutos -= horas * 60
            self.fields['dias'].initial = dias
            self.fields['horas'].initial = horas
            self.fields['minutos'].initial = minutos

    def clean(self):
        cleaned_data = super().clean()
        color = cleaned_data.get('color')
        if not color:
            self.add_error('color', _('Valor requerido'))
