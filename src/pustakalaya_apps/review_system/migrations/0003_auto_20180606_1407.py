# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-06 08:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review_system', '0002_review_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created']},
        ),
        migrations.AlterField(
            model_name='review',
            name='content_type',
            field=models.CharField(editable=False, max_length=20, null=True),
        ),
    ]
