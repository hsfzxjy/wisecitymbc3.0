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

    # def __eq__(self, obj):
    #     if isinstance(obj, Enum):
    #         return super(Enum, self).__eq__(obj)

    #     return self.value == obj

    def __gt__(self, obj):
        return self.value > getattr(obj, 'value', obj)

    __lt__ = lambda self, obj: getattr(obj, 'value', obj) > self.value
