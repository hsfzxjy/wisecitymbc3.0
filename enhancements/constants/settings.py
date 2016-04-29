from django.conf import settings

OUTPUT_PATHS = list(getattr(settings, 'CONSTS_OUTPUT_PATHS', []))
