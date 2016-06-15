from django.db import models
from django.db.models import signals
from django.conf import settings
from django.dispatch import receiver

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
    replies_count = models.IntegerField(
        _('replies count'),
        default=0
    )

    def close(self):
        self.is_closed = True
        self.save()

    def open(self):
        self.is_closed = False
        self.save()

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


@receiver(signals.post_save, sender=Reply)
def reply_saved_handler(sender, instance, created, **kwargs):
    if not created:
        return

    topic = instance.topic
    topic.replies_count += 1
    topic.updated_time = instance.created_time

    topic.save()


@receiver(signals.post_delete, sender=Reply)
def reply_deleted_handler(sender, instance, **kwargs):
    topic = instance.topic

    topic.replies_count -= 1
    topic.updated_time = instance.created_time

    topic.save()
