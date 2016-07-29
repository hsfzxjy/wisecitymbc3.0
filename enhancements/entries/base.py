from functools import partial


class BaseEntries(object):

    @classmethod
    def expose(cls):
        instance = cls()

        return (
            instance,
            instance.register,
            instance.unregister,
            instance.exists,
        )

    def _post_register(self, *args, **kwargs):
        pass


class BaseListEntries(BaseEntries, list):

    def register(self, item):
        if self.exists(item):
            raise KeyError('Duplicated key %r.' % item)

        self.append(item)
        self._post_register(item)

        return item

    def unregister(self, item):
        self.remove(item)

    def exists(self, item):
        return item in self


class BaseDictEntries(BaseEntries, dict):

    def register(self, key, value=None):
        if self.exists(key):
            raise KeyError('Duplicated key %r.' % key)

        if value is None:
            return partial(self.register, key)

        self[key] = value
        self._post_register(key, value)

        return value

    def unregister(self, key):
        self.pop(key, None)

    def get_value(self, key, default=None):
        return self.get(key, default)

    def exists(self, key):
        return key in self

    @classmethod
    def expose(cls):
        exposed = super(BaseDictEntries, cls).expose()
        return exposed + (exposed[0].get_value, )
