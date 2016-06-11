from threading import Lock


class RegistryBase(object):

    def __init__(self):
        self.__dict = {}
        self.__lock = Lock()

    def make_key(self, key):
        return key

    def register(self, key, value=None):
        with self.__lock:
            self.__dict[self.make_key(key)] = value
            self.do_registered(key, value)

    def do_registered(self, key, value=None):
        pass

    def unregister(self, key):
        with self.__lock:
            del self.__dict[self.make_key(key)]
            self.do_unregistered(key)

    def do_unregistered(self, key):
        pass

    def is_registered(self, key):
        return self.make_key(key) in self.__dict

    @property
    def keys(self):
        return list(self.__dict.keys())

    @property
    def items(self):
        return list(self.__dict.items())

    def get_value(self, key, default=None):
        return self.__dict.get(self.make_key(key), default)
