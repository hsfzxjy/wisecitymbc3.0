from django.db import models
from django.conf import settings

from enhancements.shortcuts import _


class Topic(models.Model):
    asker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('asker')
    )
    title = models.CharField(
        _('title'),
        max_length=1000,
    )
    created_time = models.DateTimeField(
        _('created time'),
        auto_now_add=True
    )
    updated_time = models.DateTimeField(
        _('updated time'),
        auto_now_add=True
    )
    is_closed = models.BooleanField(
        _('is closed'),
        default=False
    )

    class Meta:
        verbose_name = _('topic')
        verbose_name_plural = _('topics')


class Reply(models.Model):
    topic = models.ForeignKey(
        'Topic',
        verbose_name=_('topic')
    )
    created_time = models.DateTimeField(
        _('created time'),
        auto_now_add=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('author')
    )
    content = models.TextField(_('content'))
    attachments = models.ManyToManyField(
        'files.File',
        verbose_name=_('attachments')
    )

    class Meta:
        verbose_name_plural = _('replies')
        verbose_name = _('reply')
