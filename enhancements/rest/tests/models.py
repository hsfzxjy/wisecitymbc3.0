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
rules.add_perm('tests.view_goods', rules.always_allow)


class Bucket(models.Model):

    goods = models.ManyToManyField(Goods)
    name = models.CharField(max_length=100)

rules.add_perm('tests.view_bucket', rules.always_true)
rules.add_perm('tests.add_bucket', rules.always_true)
rules.add_perm('tests.change_bucket', rules.always_true)


class Ball(models.Model):

    box = models.ForeignKey('Box', related_name='balls')

rules.add_perm('tests.view_ball', rules.always_true)
rules.add_perm('tests.add_ball', rules.always_true)
rules.add_perm('tests.change_ball', rules.always_true)
rules.add_perm('tests.view_box', rules.always_true)
rules.add_perm('tests.change_box', rules.always_true)
rules.add_perm('tests.add_box', rules.always_true)


class Box(models.Model):

    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('id',)
