from enum import Enum as _Enum


class Enum(_Enum):
    """Django capatible Enum"""

    def deconstruct(self):
        cls = self.__class__
        return (
            '.'.join([cls.__module__, cls.__name__]),
            [self.value],
            {}
        )

    def __str__(self):
        return str(self.value)

    def __eq__(self, obj):
        try:
            hash(obj)
        except TypeError:
            return False
        else:
            return obj == self.value or hash(self) == hash(obj)

    def __hash__(self):
        return hash(self._name_)

    def __gt__(self, obj):
        return self.value > getattr(obj, 'value', obj)

    __lt__ = lambda self, obj: getattr(obj, 'value', obj) > self.value
