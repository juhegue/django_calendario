# -*- coding: utf-8 -*-

import logging
from datetime import timedelta
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from post_office import mail
from calendario.models import AgendaEvento
from calendario.util.notificacionfcm import NotificacionFcm

HORAS_MARGEN_COMPLETO = 12
MINUTOS_MARGEN_PARCIAL = 30


logger = logging.getLogger(__name__)


def envia_movil(qevento):
    inicio = timezone.localtime(qevento.inicio).strftime('%H:%M')
    finhora = timezone.localtime(qevento.fin).strftime('%H:%M')
    fin = timezone.localtime(qevento.fin).strftime('%d/%m/%Y %H:%M')

    periodo = f'Desde {inicio}'
    if qevento.fin:
        if qevento.inicio.date() == qevento.fin.date():
            periodo += f' Hasta {finhora}'
        else:
            periodo += f' Hasta {fin}'

    logger.info(f"envia_movil:{periodo}")
    n = NotificacionFcm(qevento.usuario)
    n.aviso('Notas notifiación', f'{periodo}\n{qevento.titulo}')


def envia_mail(qevento):
    inicio = timezone.localtime(qevento.inicio).strftime('%H:%M')
    finhora = timezone.localtime(qevento.fin).strftime('%H:%M')
    fin = timezone.localtime(qevento.fin).strftime('%d/%m/%Y %H:%M')

    periodo = f'Desde{inicio}'
    if qevento.fin:
        if qevento.inicio.date() == qevento.fin.date():
            periodo += f' Hasta {finhora}'
        else:
            periodo += f' Hasta {fin}'

    logger.info(f"envia_mail:{periodo}")
    mail.send(
        recipients=qevento.usuario.email,
        subject=f'Aviso: {qevento.titulo}',
        message=f'{periodo}\n{qevento.titulo}',
        html_message=f'<h3>{periodo}</h3><br>{qevento.titulo}',
    )


def procesa_eventos():
    ahora = timezone.now()

    logger.info(f"procesa_eventos {ahora.strftime('%Y/%m/%d, %H:%M:%S')}")

    inicio = ahora + timedelta(hours=HORAS_MARGEN_COMPLETO)
    for qevento in AgendaEvento.objects.filter(dia_completo=True,
                                               inicio__lte=inicio,
                                               fin__gte=ahora):
        logger.info(f"evento:{qevento.id}")
        if qevento.aviso_email and not qevento.email_enviado:
            envia_mail(qevento)
            qevento.email_enviado = ahora
            qevento.save()

        if qevento.aviso_movil and not qevento.movil_enviado:
            envia_movil(qevento)
            qevento.movil_enviado = ahora
            qevento.save()

    inicio = ahora + timedelta(minutes=MINUTOS_MARGEN_PARCIAL)
    for qevento in AgendaEvento.objects.filter(dia_completo=False,
                                               inicio__lte=inicio,
                                               fin__gte=ahora):
        logger.info(f"evento:{qevento.id}")
        if qevento.aviso_email and not qevento.email_enviado:
            envia_mail(qevento)
            qevento.email_enviado = ahora
            qevento.save()

        if qevento.aviso_movil and not qevento.movil_enviado:
            envia_movil(qevento)
            qevento.movil_enviado = ahora
            qevento.save()

    inicio = ahora - timedelta(minutes=1)
    for qevento in AgendaEvento.objects.filter(inicio_enviado__isnull=True,
                                               inicio__gte=inicio,
                                               inicio__lte=ahora):
        logger.info(f"evento:{qevento.id}")
        if qevento.aviso_email:
            envia_mail(qevento)

        if qevento.aviso_movil:
            envia_movil(qevento)

        qevento.inicio_enviado = ahora
        qevento.save()


def start():     # Añadir el start en apps.py
    # TODO:: con Gunicorn se inicia varias veces, se usa un socket TCP para evitar esto
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 43210))

        logger.info("scheduler iniciado")
        scheduler = BackgroundScheduler()
        scheduler.add_job(procesa_eventos, 'interval', minutes=1)
        scheduler.start()

    except socket.error:
        logger.info("¡scheduler ya iniciado!, NADA QUE HACER")

