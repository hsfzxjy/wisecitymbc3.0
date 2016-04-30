from django.db import models
from django.conf import settings

from .consts import ARTICLE_TYPE_CHOICES, ArticleType


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField('Tag')
    content = models.TextField()
    is_top = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    attachments = models.ManyToManyField('files.File')
    article_type = models.IntegerField(
        ARTICLE_TYPE_CHOICES, default=ArticleType.government.value)


class Tag(models.Model):
    name = models.CharField(max_length=255)
