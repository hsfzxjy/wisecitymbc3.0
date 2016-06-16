from django.db import models
from django.db.models import signals
from django.core.exceptions import ValidationError
from django.dispatch import receiver

from enhancements.models.fields import EnumField
from enhancements.models.mixins import AutoCleanMixin
from enhancements.shortcuts import _

from . import consts, utils

import os.path
from urllib.parse import urlunsplit


class File(AutoCleanMixin, models.Model):

    path = models.CharField(_('file path'), max_length=4096)
    file_name = models.CharField(_('file name'), max_length=4096, blank=True)
    storage_url = models.URLField(_('url'), blank=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    mime_type = models.CharField(_('mime type'), max_length=255, blank=True)
    file_type = EnumField(consts.FileType,
                          verbose_name=_('file type'),
                          default=consts.FileType.file)

    def clean(self):
        if not self.path:
            raise ValidationError('path cannot be blank.')

        self.mime_type = utils.get_mime_type(self.path)
        self.file_name = os.path.basename(self.path)
        self.file_type = consts.FileType.get_by_mime_type(self.mime_type)
        self.storage_url = urlunsplit(
            ('http', utils.domain_name, self.path, '', '')
        )


@receiver(signals.post_delete, sender=File)
def file_post_delete(sender, instance, **kw):
    utils.delete_file(instance.path)
