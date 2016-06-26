from django.db import models
from django.contrib.contenttypes import fields as contenttypes_fields

from enhancements.shortcuts import _

from jsonfield import JSONField

from django.conf import settings

from enhancements.utils.types import is_int_list


def validate_list(qs, lst):
    assert is_int_list(lst) or isinstance(lst, models.QuerySet), \
        "list<int> or QuerySet expected, got %r." % type(lst)

    if is_int_list(lst):
        return qs.filter(pk__in=lst) if lst else qs
    else:
        return lst


class NotificationQuerySet(models.QuerySet):

    def mark_as_read(self, lst):
        qs = validate_list(self, lst)
        return qs.update(has_read=True)

    def mark_all_as_read(self):
        return self.update(has_read=True)


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_('receiver'),
                             related_name='notifications')
    template = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    data = JSONField()
    has_read = models.BooleanField(default=False)
    url = models.URLField(_('URL'))

    target_id = models.PositiveIntegerField(null=True)
    target_content_type = models.ForeignKey(
        'contenttypes.ContentType', null=True)
    target = contenttypes_fields.GenericForeignKey(
        'target_content_type',
        'target_id'
    )

    module = models.CharField(_('module'), max_length=255)

    objects = NotificationQuerySet.as_manager()

    @property
    def message(self):
        if hasattr(self, '_message'):
            return self._message

        from . import formatter
        self._message = formatter.render(self.template, self.data)

        return self._message

    def mark_as_read(self):
        self.has_read = True
        self.save()

    def __str__(self):
        return self.message
