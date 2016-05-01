

__all__ = ['register', 'unregister',
           'has_module', 'RegistryError', 'get_modules']

modules = []


class RegistryError(Exception):
    pass


def has_module(module):
    return module in modules


def register(module, silent=True):

    if has_module(module):
        if silent:
            return
        else:
            raise RegistryError("Module %r has registered." % module)

    modules.append(module)


def unregister(module, silent=True):

    if not has_module(module):
        if silent:
            return
        else:
            raise RegistryError("Module %r not found." % module)

    modules.remove(module)


def get_modules():
    return tuple(modules)
