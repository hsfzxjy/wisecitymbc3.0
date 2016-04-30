from django.utils.module_loading import module_has_submodule, import_module
from django.utils.itercompat import is_iterable
from django.apps import apps

from enum import EnumMeta


def generate_consts():
    consts = collect_consts()

    from . import settings
    import json

    for path in settings.OUTPUT_PATHS:
        with open(path, 'w') as fp:
            json.dump(consts, fp)


def collect_consts():
    consts_dict = {}

    for app in apps.get_app_configs():
        if not module_has_submodule(app.module, 'consts'):
            continue

        consts = get_consts(import_module('%s.consts' % app.name))

        if not consts:
            continue

        consts_dict[app.label] = consts

    return consts_dict


def get_consts(mod):
    export_names = getattr(mod, 'EXPORTS', [])

    if not is_iterable(export_names):
        raise TypeError('`%s.EXPORTS` must be an iterable.' % mod.__name__)

    consts = {}

    for name in export_names:
        consts[name] = parse(getattr(mod, name))

    return consts


def parse(obj):
    if isinstance(obj, EnumMeta):
        return {
            item.name: item.value
            for item in obj
        }
    else:
        return obj
