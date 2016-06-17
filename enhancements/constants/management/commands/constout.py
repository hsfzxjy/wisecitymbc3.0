from django.core.management import BaseCommand

from enhancements.constants.core import generate_consts


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        generate_consts()
