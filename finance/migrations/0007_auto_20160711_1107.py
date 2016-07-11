# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-11 11:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_auto_20160710_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='bond',
            name='updated_time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 7, 11, 11, 6, 57, 23071)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='futures',
            name='updated_time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 7, 11, 11, 7, 8, 319069)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rawmaterials',
            name='updated_time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 7, 11, 11, 7, 14, 664001)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stock',
            name='updated_time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 7, 11, 11, 7, 19, 135233)),
            preserve_default=False,
        ),
    ]
