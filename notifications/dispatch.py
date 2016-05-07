from .models import Notification

from functools import partial

from . import formatter, registry


def send(user, template, url, module, target=None, **kwargs):
    """send notification.

    The core method to send a notification

    Arguments:
        user {User} -- The receiver.
        template {str} -- The message template.
        url {str} -- The corresponding URL.
        module {str} -- The logical group.
        **kwargs {dict} -- Exrta data for template rendering.
    """

    if not registry.has_module(module):
        raise registry.RegistryError("Module %r not found." % module)

    Notification.objects.create(
        user=user,
        template=template,
        url=url,
        module=module,
        target=target,
        data=formatter.extract_variables(
            template,
            user=user,
            url=url,
            module=module,
            target=target,
            **kwargs
        )
    )


class Sender(object):

    def __init__(self, *args, **kwargs):
        self.__args = args
        self.__kwargs = kwargs

    def _extend_arguments(self, *_args, **_kwargs):
        from copy import deepcopy

        args = deepcopy(list(self.__args))
        kwargs = deepcopy(_kwargs)

        args.extend(_args)
        kwargs.update(kwargs)

        return args, kwargs

    def pack(self, *args, **kwargs):

        a, k = self._extend_arguments(*args, **kwargs)

        return Sender(*a, **k)

    def send(self, *args, **kwargs):

        a, k = self._extend_arguments(*args, **kwargs)

        return send(*a, **k)
