from django.db import models

from enhancements.auth.models import AbstractUser


class User(AbstractUser):

    nickname = models.CharField(max_length=255, unique=True)
