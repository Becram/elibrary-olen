# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-18 06:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0030_auto_20180607_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='videofileupload',
            name='video_running_length',
            field=models.CharField(blank=True, editable=False, max_length=255, null=True, verbose_name='Video running length'),
        ),
    ]
