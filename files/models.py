from django.db import models

from . import consts


class File(models.Model):
    file_name = models.CharField(max_length=4096)
    storage_url = models.URLField()
    created_time = models.DateTimeField(auto_now_add=True)
    mime_type = models.CharField(max_length=255)
    file_type = models.IntegerField(choices=consts.FILE_TYPE_CHOICES)
