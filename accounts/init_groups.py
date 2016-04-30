from django.contrib.auth.models import Group


def create_default_groups():
    from .consts import UserType

    for item in UserType:
        Group.objects.get_or_create(name=item.name)
