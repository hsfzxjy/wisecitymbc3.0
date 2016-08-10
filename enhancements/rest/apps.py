from django.apps import AppConfig

from . import viewsets, serializers, serializer_fields

# serializer_fields.monkey_patch()
# serializers.monkey_patch()
# viewsets.monkey_patch()


class AutoDiscoverConfig(AppConfig):

    name = 'enhancements.rest'

    def ready(self):
        from django.utils.module_loading import autodiscover_modules

        for module_name in ['serializers', 'viewsets', 'views']:
            autodiscover_modules(module_name)
