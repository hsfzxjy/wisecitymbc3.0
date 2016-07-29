from django.db import models

from enhancements.models.mixins import LimitedAccessMixin


class BasicModel(LimitedAccessMixin, models.Model):

    text = models.TextField()
    name = models.CharField(max_length=100)

    NON_ACCESSIBLE = {
        'rest_test.view_basicmodel': ['name']
    }

    def get_absolute_url(self):
        return 'test_url'


class ManyToManyTarget(LimitedAccessMixin, models.Model):

    name = models.CharField(max_length=100)

    NON_ACCESSIBLE = {
        'rest_test.view_manytomanytarget': ['name']
    }


class ManyToManySource(models.Model):

    name = models.CharField(max_length=100)
    targets = models.ManyToManyField(ManyToManyTarget)


class ForeignKeyTarget(models.Model):

    name = models.CharField(max_length=100)

    @property
    def custom_name(self):
        return 'custom %s' % self.name


class ForeignKeySource(models.Model):

    name = models.CharField(max_length=100)
    target = models.ForeignKey(ForeignKeyTarget)
