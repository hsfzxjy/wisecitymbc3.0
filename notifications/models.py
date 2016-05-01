from django.db import models
from django.contrib.contenttypes import fields as contenttypes_fields

from jsonfield import JSONField

from django.conf import settings


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    template = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    data = JSONField()
    has_read = models.BooleanField(default=False)
    url = models.URLField()

    target_id = models.PositiveIntegerField(null=True)
    target_content_type = models.ForeignKey(
        'contenttypes.ContentType', null=True)
    target = contenttypes_fields.GenericForeignKey(
        'target_content_type',
        'target_id'
    )

    module = models.CharField(max_length=255)
