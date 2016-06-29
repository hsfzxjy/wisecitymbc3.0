from django.db import models

from enhancements.collections import Enum


class EnumField(models.PositiveIntegerField):
    """EnumField

    A wrapper field class for `Enum`. Optionally require
    the target class have a `get_choices` classmethod, which returns
    a map representing the `CHOICES` map.

    Extends:
        models.PositiveIntegerField
    """

    def __init__(self, enum, *args, **kwargs):
        self._enum = enum

        assert issubclass(self._enum, Enum)

        try:
            self._choices = kwargs['choices']
        except KeyError:
            if hasattr(self._enum, 'get_choices'):
                self._choices = self._enum.get_choices()

                if isinstance(self._choices, dict):
                    from enhancements.constants.utils import annotate

                    self._choices = annotate(self._choices)

                kwargs['choices'] = self._choices
            else:
                self._choices = []

        super(EnumField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(EnumField, self).deconstruct()

        args.insert(0, self._enum)

        return name, path, args, kwargs

    def _parse(self, value):
        """
        Take an int and parse it into enum value.
        """

        assert isinstance(value, int)

        return self._enum(value)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value

        return self._parse(value)

    def to_python(self, value):
        if isinstance(value, self._enum):
            return value

        if value is None:
            return value

        return self._parse(value)

    def get_prep_value(self, enum_value):
        return enum_value.value if isinstance(enum_value, Enum) \
            else self._enum(int(enum_value)).value

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)
