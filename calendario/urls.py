# -*- coding: utf-8 -*-

from django.urls import path

from .views import CalendarioView, \
    EventoPredefinidoListView, EventoPredefinidoCreateView, EventoPredefinidoUpdateView, EventoPredefinidoDeleteView


urlpatterns = [
    path('calendario/', CalendarioView.as_view(), name="calendario"),
    path('calendario/predefinidos/', EventoPredefinidoListView.as_view(), name="evento_predefinido_lista"),
    path('calendario/predefinidos/nuevo/', EventoPredefinidoCreateView.as_view(), name="evento_predefinido_nuevo"),
    path('calendario/predefinidos/edita/<slug:pk>/', EventoPredefinidoUpdateView.as_view(),
         name="evento_predefinido_edita"),
    path('calendario/predefinidos/elimina/<slug:pk>/', EventoPredefinidoDeleteView.as_view(),
         name="evento_predefinido_elimina"),
]
