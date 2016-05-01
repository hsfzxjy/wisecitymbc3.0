from django.db import models
from django.conf import settings


class Topic(models.Model):
    asker = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)


class Reply(models.Model):
    topic = models.ForeignKey('Topic')
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()
    attachments = models.ManyToManyField('files.File')
