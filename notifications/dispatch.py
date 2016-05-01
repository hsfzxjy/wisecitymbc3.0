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


def Sender(**kwargs):
    return partial(send, **kwargs)
