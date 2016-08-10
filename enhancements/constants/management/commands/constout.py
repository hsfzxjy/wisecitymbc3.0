from django.utils import translation
from django.conf import settings
from django.core.management import BaseCommand

from enhancements.constants.core import generate_consts


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        translation.activate(settings.LANGUAGE_CODE)
        generate_consts()

        translation.deactivate()
