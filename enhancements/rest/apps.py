from django.apps import AppConfig


class AutoDiscoverConfig(AppConfig):

    name = 'enhancements.rest'

    def ready(self):
        from django.utils.module_loading import autodiscover_modules

        autodiscover_modules('viewsets')
