from django.db import models

from enhancements.auth.models import AbstractUser

from .consts import USER_TYPE_CHOICES, UserType


class User(AbstractUser):

    nickname = models.CharField(max_length=255, unique=True)
    data = models.ForeignKey('UserData', null=True, blank=True)
    user_type = models.IntegerField(
        choices=USER_TYPE_CHOICES, default=UserType.company.value)


class UserData(models.Model):
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)
    description = models.TextField()
    reports = models.ManyToManyField('files.File')
