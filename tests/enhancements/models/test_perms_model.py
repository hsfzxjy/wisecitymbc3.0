from django.test import TestCase

from enhancements.models.mixins import PermsMixin
from django.db import models


class M(models.Model, PermsMixin):

    f1 = models.IntegerField()
    f2 = models.IntegerField()

    INVISIBLE_FIELDS = {
        'a': ['f1'],
        'b': []
    }


class M2(models.Model, PermsMixin):

    f1 = models.IntegerField()
    f2 = models.IntegerField()

    INVISIBLE_FIELDS = {
        ('b', 'c'): ['id', ]
    }

    DEFAULT_ID = False


class PermsModelTestCase(TestCase):

    def test_model(self):
        self.assertEqual(M.get_invisible_fields(), {
            'a': {'f1'},
            'b': set(),
        })
        self.assertEqual(M2.get_invisible_fields(), {
            'b': {'id'},
            'c': {'id'},
        })
