from django.test import TestCase

from enhancements.models.mixins import PermsMixin
from django.db import models


class M(models.Model, PermsMixin):

    f1 = models.IntegerField()
    f2 = models.IntegerField()

    PERMS = {
        'a': {
            'visible': ['f1'],
        },
        'b': {

        }
    }


class M2(models.Model, PermsMixin):

    f1 = models.IntegerField()
    f2 = models.IntegerField()

    PERMS = {
        'a': {
            'visible': ['f1'],
        },
        ('b', 'c'): {
            'invisible': ['id', ],
        }
    }

    DEFAULT_ID = False


class PermsModelTestCase(TestCase):

    def test_model(self):
        self.assertEqual(M.get_perms_map(), {
            'a': {'f1', 'id'},
            'b': {'f1', 'f2', 'id'},
        })
        self.assertEqual(M2.get_perms_map(), {
            'a': {'f1'},
            'b': {'f1', 'f2'},
            'c': {'f1', 'f2'},
        })
