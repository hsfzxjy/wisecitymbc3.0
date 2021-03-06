# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-16 11:11
from __future__ import unicode_literals

from django.db import migrations, models
import enhancements.models.fields
import files.consts


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_auto_20160610_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created time'),
        ),
        migrations.AlterField(
            model_name='file',
            name='file_name',
            field=models.CharField(max_length=4096, verbose_name='file name'),
        ),
        migrations.AlterField(
            model_name='file',
            name='file_type',
            field=enhancements.models.fields.EnumField(files.consts.FileType, choices=[(files.consts.FileType(1), 'video'), (files.consts.FileType(2), 'image'), (files.consts.FileType(3), 'file')], default=files.consts.FileType(3), verbose_name='file type'),
        ),
        migrations.AlterField(
            model_name='file',
            name='mime_type',
            field=models.CharField(max_length=255, verbose_name='mime type'),
        ),
        migrations.AlterField(
            model_name='file',
            name='storage_url',
            field=models.URLField(verbose_name='url'),
        ),
    ]
