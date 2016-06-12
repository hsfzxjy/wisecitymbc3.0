from django.apps import AppConfig

from . import viewsets, serializers

serializers.monkey_patch()
viewsets.monkey_patch()


class AutoDiscoverConfig(AppConfig):

    name = 'enhancements.rest'

    def ready(self):
        from django.utils.module_loading import autodiscover_modules

        autodiscover_modules('serializers')
        autodiscover_modules('viewsets')
