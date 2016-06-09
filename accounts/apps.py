from django.apps import AppConfig

from enhancements.shortcuts import _


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = _('accounts')

    def ready(self):
        from django.db.utils import ProgrammingError

        from .init_groups import create_default_groups

        try:
            create_default_groups()
        except ProgrammingError:
            pass
