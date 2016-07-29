from django.test import TestCase

from enhancements.models.mixins import LimitedAccessMixin
from django.db import models


class M(models.Model, LimitedAccessMixin):

    f1 = models.IntegerField()
    f2 = models.IntegerField()

    NON_ACCESSIBLE = {
        'a': ['f1'],
        'b': []
    }


class M2(models.Model, LimitedAccessMixin):

    f1 = models.IntegerField()
    f2 = models.IntegerField()

    NON_ACCESSIBLE = {
        ('b', 'c'): ['id', ]
    }

    DEFAULT_ID = False


class PermsModelTestCase(TestCase):

    def test_model(self):
        self.assertEqual(M._get_non_accessible_fields(), {
            'a': {'f1'},
            'b': set(),
        })
        self.assertEqual(M2._get_non_accessible_fields(), {
            'b': {'id'},
            'c': {'id'},
        })
