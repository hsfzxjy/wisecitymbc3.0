from django.db import models
from django.db.models import signals
from django.conf import settings
from django.dispatch import receiver

from enhancements.shortcuts import _
from enhancements.models.mixins import AutoURLMixin
from enhancements.utils.lock import pass_if_locked, LockMixin
from enhancements.utils.html import filter_html_mixin

from accounts.models import User

from .dispatchers import notifier

FilterContentMixin = filter_html_mixin(['content'])


class Topic(AutoURLMixin, LockMixin, FilterContentMixin, models.Model):
    asker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('asker')
    )
    title = models.CharField(
        _('title'),
        max_length=1000,
    )
    content = models.TextField(_('content'))
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
    attachments = models.ManyToManyField(
        'files.File',
        verbose_name=_('attachments')
    )

    def __init__(self, *args, **kwargs):
        super(Topic, self).__init__(*args, **kwargs)

        self.updating_lock = self.locks['updating']

    def _notify_close_open(self, action, executer):
        notifier.select('{0}_topic'.format(action)).send(
            user=User.objects.governments_or(
                self.asker).exclude(pk=executer.pk),
            target=self
        )

    def close(self, executer):
        self.is_closed = True
        self.updating_lock.lock()
        self._notify_close_open('close', executer)
        self.save()

    def open(self, executer):
        self.is_closed = False
        self.updating_lock.lock()
        self._notify_close_open('open', executer)
        self.save()

    class Meta:
        verbose_name = _('topic')
        verbose_name_plural = _('topics')

    def get_absolute_url(self):
        return '/detail/topics/{0}/'.format(self.id)


class Reply(AutoURLMixin, FilterContentMixin, models.Model):
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

    def get_absolute_url(self):
        return '/detail/topics/{0}/'.format(self.topic.id)


@receiver(signals.post_save, sender=Reply)
def reply_saved_handler(sender, instance, created, **kwargs):
    if not created:
        return

    topic = instance.topic
    topic.replies_count += 1
    topic.updated_time = instance.created_time

    topic.save()
    notifier.select('create_reply').send(
        user=User.objects.governments_or(
            topic.asker).exclude(pk=instance.author.pk),
        target=instance
    )


@receiver(signals.post_save, sender=Topic)
@pass_if_locked('updating')
def topic_send_n(sender, instance, created, update_fields, **kwargs):
    notifier.select('create_topic' if created else 'update_topic').send(
        user=User.objects.governments(),
        target=instance
    )


@receiver(signals.post_delete, sender=Reply)
def reply_deleted_handler(sender, instance, **kwargs):
    from datetime import datetime

    topic = instance.topic

    topic.replies_count -= 1
    topic.updated_time = datetime.now()

    topic.save()
