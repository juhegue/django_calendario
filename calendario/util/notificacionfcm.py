# -*- coding: utf-8 -*-

import logging
import time

from pyfcm import FCMNotification
from django.conf import settings

logger = logging.getLogger(__name__)


class NotificacionFcm(object):
    def __init__(self, usuario):
        self.usuario = usuario

    def _envia(self, msg_title, msg_body, data_extra=None):
        server_key = settings.FIREBASE_SERVER_KEY
        fcm_token = self.usuario.fcm.token
        if fcm_token and self.usuario.is_active:
            data = {
                "title": msg_title,
                "body": msg_body,
            }

            if data_extra:
                data.update(data_extra)

            try:
                result = FCMNotification(api_key=server_key). \
                    notify_single_device(registration_id=fcm_token,
                                         message_title=msg_title,
                                         message_body=msg_body,
                                         # message_icon=msg_icon,
                                         data_message=data,
                                         click_action="FLUTTER_NOTIFICATION_CLICK",
                                         sound="Default")
                logger.info("NotificacionFcm[RESULT]: %s" % result)

            except Exception as e:
                logger.error("NotificacionFcm[ERROR]: %s" % e)

    def demo(self):
        title = 'Demo de calendario'
        body = '¡Hola Mundo, esto solo es una prueba!'
        self._envia(title, body)

    def aviso(self, title, body):
        self._envia(title, body)
