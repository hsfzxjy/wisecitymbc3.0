from django.db import models


class Base(models.Model):

    name = models.CharField(max_length=255)
    child = models.ForeignKey('Child')


class Child(models.Model):

    def get_absolute_url(self):
        return '/' + self.id
