from django.db import models
from django.contrib.contenttypes import fields as ct_fields

from django.conf import settings


class Entry(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    target_id = models.PositiveIntegerField()
    target_content_type = models.ForeignKey(
        'contenttypes.ContentType')
    target = ct_fields.GenericForeignKey(
        'target_content_type',
        'target_id',
    )

    created_time = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField()
