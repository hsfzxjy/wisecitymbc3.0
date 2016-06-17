from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class NotificationsConfig(AppConfig):
    name = 'notifications'

    def ready(self):
        autodiscover_modules('dispatchers')
