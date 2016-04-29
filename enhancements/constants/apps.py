from django.apps import AppConfig


class ConstantsConfig(AppConfig):
    name = 'constants'

    def ready(self):
        from .core import generate_consts

        generate_consts()
