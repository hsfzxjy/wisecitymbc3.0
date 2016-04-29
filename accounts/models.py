from django.db import models

from enhancements.auth.models import AbstractUser


class User(AbstractUser):

    nickname = models.CharField(max_length=255, unique=True)
    data = models.ForeignKey('UserData', null=True, blank=True)


class UserData(models.Model):
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)
    description = models.TextField()
