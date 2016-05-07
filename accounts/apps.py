from django.apps import AppConfig

from enhancements.shortcuts import _


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = _('accounts')

    def ready(self):
        from .init_groups import create_default_groups

        create_default_groups()
