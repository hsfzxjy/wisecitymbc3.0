from django.apps import apps
from django.http import Http404
from django.shortcuts import get_object_or_404


def make_name(model, action, id=''):
    return '{app_label}_{model}_{action}_{id}'.format(
        model=model._meta.model_name.lower(),
        app_label=model._meta.app_label,
        action=action,
        id=id
    )


def get_perms(user):
    models = apps.get_models()
    result = {}

    for model in models:
        model_name = model._meta.model_name.lower()

        for action in ['add', 'view']:
            name = '{app_label}.{action}_{model}'.format(
                app_label=model._meta.app_label,
                model=model_name,
                action=action
            )
            result[make_name(model, action)] = user.has_perm(name)

    return result


def get_object_perms(user, model_path, id):

    try:
        model = apps.get_model(model_path)
    except LookupError:
        raise Http404

    obj = get_object_or_404(model, pk=id)

    result = {}

    for action in ['view', 'change', 'delete']:
        name = '{app_label}.{action}_{model}'.format(
            app_label=model._meta.app_label,
            model=model._meta.model_name.lower(),
            action=action
        )
        result[make_name(model, action, id)] = user.has_perm(name, obj)

    return result
