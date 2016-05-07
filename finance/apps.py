from django.apps import AppConfig

from enhancements.shortcuts import _


class FinanceConfig(AppConfig):
    name = 'finance'
    verbose_name = _('Finance System')
