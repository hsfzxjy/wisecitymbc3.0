from django.core.management import call_command, BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        from enhancements.postgres import init_zhparser

        init_zhparser()
        call_command('migrate')
        call_command('installwatson')
        call_command('buildwatson')
