from inflection import camelize, underscore

from django.apps import apps
from django.http import Http404
from django.shortcuts import get_object_or_404

from collections import defaultdict

__all__ = ['default_perms', 'model_perms']


def tree():
    return defaultdict(tree)


def model_info(model_class):
    return model_class._meta.app_label, model_class.__name__


def store_permission(storage, user, action, model, id=None):
    app, name = model_info(model)
    permission_name = '{0}.{1}_{2}'.format(app, action, name.lower())

    if id is None:
        storage[app][underscore(name)][action] = user.has_perm(permission_name)
    else:
        obj = get_object_or_404(model, pk=id)
        storage[app][underscore(name)][id][action] = user.has_perm(
            permission_name, obj)


def get_model_class(app, name):
    try:
        return apps.get_model(app, camelize(name))
    except LookupError:
        raise Http404


# Permissions getters & formatters

def default_perms(user):
    all_models = apps.get_models()
    result = tree()

    for model in all_models:
        for action in ('add', 'view'):
            store_permission(result, user, action, model)

    return result


def model_perms(user, app, name, id=None):
    model = get_model_class(app, name)
    result = tree()

    for action in ('add', 'view', 'change', 'delete'):
        store_permission(result, user, action, model, id)

    return result
