from enhancements.globalreg.core import RegistryBase

__all__ = ['registry']


class SerializerRegistry(RegistryBase):

    def make_key(self, key):
        return key.__name__

registry = SerializerRegistry()
