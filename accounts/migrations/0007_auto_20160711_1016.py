# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-11 10:16
from __future__ import unicode_literals

import accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20160710_2314'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', accounts.models.UserQuerySet.as_manager()),
            ],
        ),
    ]
