from .models import Notification

from django.utils.itercompat import is_iterable

from . import formatter, registry


def send(user, template, module, url=None, target=None, **kwargs):
    """send notification.

    The core method to send a notification

    Arguments:
        user {User} -- The receiver.
        template {str} -- The message template.
        url {str} -- The corresponding URL.
        module {str} -- The logical group.
        **kwargs {dict} -- Exrta data for template rendering.
    """

    def get_arguments(user):
        return dict(
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

    if url is None:
        url = target.get_absolute_url()

    if not registry.has_module(module):
        raise registry.RegistryError("Module %r not found." % module)
    print(user)
    if is_iterable(user):
        args = []
        for u in user:
            args.append(get_arguments(u))

        return Notification.objects.bulk_create(
            map(lambda arg: Notification(**arg), args)
        )
    else:
        return Notification.objects.create(**get_arguments(user))


class Sender(object):

    def __init__(self, templates=None, *args, **kwargs):
        self.__templates = templates if templates is not None else {}
        self.__args = args
        self.__kwargs = kwargs

    def _extend_arguments(self, *_args, **_kwargs):
        from copy import deepcopy

        args = deepcopy(list(self.__args))
        kwargs = deepcopy(self.__kwargs)

        args.extend(_args)
        kwargs.update(_kwargs)

        return args, kwargs

    def pack(self, *args, **kwargs):

        a, k = self._extend_arguments(*args, **kwargs)

        return Sender(self.__templates, *a, **k)

    def select(self, template_name):

        a, k = self._extend_arguments(
            **dict(template=self.__templates[template_name]))

        return Sender(self.__templates, *a, **k)

    def send(self, *args, **kwargs):

        a, k = self._extend_arguments(*args, **kwargs)

        return send(*a, **k)
