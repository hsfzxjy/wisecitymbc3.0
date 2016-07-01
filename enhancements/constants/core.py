from django.utils.module_loading import module_has_submodule, import_module
from django.utils.functional import Promise
from django.utils.translation import force_text
from django.utils.itercompat import is_iterable
from django.apps import apps

from enhancements.collections import Enum

from collections import OrderedDict


def generate_consts():
    consts = collect_consts()

    from . import settings
    import json

    for path in settings.OUTPUT_PATHS:
        with open(path, 'w') as fp:
            print(consts)
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
    if isinstance(obj, type(Enum)):
        return OrderedDict({
            item.name: item.value
            for item in obj
        })
    elif isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, dict):
        return OrderedDict({
            parse(key): parse(value)
            for key, value in obj.items()
        })
    elif isinstance(obj, (list, tuple)):
        return [parse(item) for item in obj]
    elif isinstance(obj, Promise):
        return force_text(obj)
    else:
        return obj
