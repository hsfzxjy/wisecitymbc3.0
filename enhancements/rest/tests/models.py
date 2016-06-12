from django.db import models
from enhancements.models.mixins import PermsMixin

import rules
from accounts import rules as accounts_rules


class Base(models.Model):

    name = models.CharField(max_length=255)
    child = models.ForeignKey('Child')


class Child(models.Model):

    def get_absolute_url(self):
        return '/' + self.id


class Goods(models.Model, PermsMixin):

    name = models.CharField(max_length=100)
    price = models.IntegerField()

    INVISIBLE_FIELDS = {
        'tests.change_goods': ['price']
    }

    class Meta:
        ordering = ('id',)

rules.add_perm('tests.change_goods', accounts_rules.is_government)
