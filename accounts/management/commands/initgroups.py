from django.core.management.base import BaseCommand, CommandError

from accounts.init_groups import create_default_groups


class Command(BaseCommand):

    help = 'Creates the default groups'

    def handle(self, *args, **options):
        self.stdout.write('Creating default groups...')
        create_default_groups()
        self.stdout.write('Done.')
