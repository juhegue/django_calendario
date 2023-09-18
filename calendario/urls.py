# -*- coding: utf-8 -*-

from django.urls import path

from .views import CalendarioView

urlpatterns = [
    path('calendario/', CalendarioView.as_view(), name="calendario"),
]
