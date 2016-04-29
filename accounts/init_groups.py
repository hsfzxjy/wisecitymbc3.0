from django.contrib.auth.models import Group

from enhancements.shortcuts import _


def create_default_groups():
    Group.objects.get_or_create(name=_('goverment'))
    Group.objects.get_or_create(name=_('company'))
    Group.objects.get_or_create(name=_('bureau'))
