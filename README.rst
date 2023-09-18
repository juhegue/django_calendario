Calendario
==========

Actualizar en settings
----------------------
* Configuración mail
* Clave firebase
* USE_TZ=True

Añadir al setting en INSTALLED_APPS
-----------------------------------
* calendario
* django_apscheduler

Añadir urls.py
--------------
* urlpatterns = [
    ...
    path('', include('calendario.urls')),
    ...
  ]
