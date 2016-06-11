from enhancements.collections import Enum
from django.db import models
from enhancements.models.fields import EnumField


class ABC(Enum):

    A = 1
    B = 2
    C = 3


class Model(models.Model):
    test = EnumField(ABC)


class ChoicesModel(models.Model):
    test = EnumField(ABC, choices=[
        (ABC.A, 'ei'),
        (ABC.B, 'bee'),
        (ABC.C, 'sii'),
    ])


class DefaultModel(models.Model):
    test = EnumField(ABC, default=ABC.C)


class ABC2(Enum):

    A = 1
    B = 2
    C = 3

    @classmethod
    def get_choices(cls):
        return {
            cls.A: 'ei',
            cls.B: 'bee',
            cls.C: 'sii'
        }


class DeclaredChoicesModel(models.Model):

    test = EnumField(ABC2)
