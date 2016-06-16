from django.db import models

from enhancements.models.fields import EnumField
from enhancements.shortcuts import _

from . import consts


class File(models.Model):
    file_name = models.CharField(_('file name'), max_length=4096)
    storage_url = models.URLField(_('url'))
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    mime_type = models.CharField(_('mime type'), max_length=255)
    file_type = EnumField(consts.FileType,
                          verbose_name=_('file type'),
                          default=consts.FileType.file)
