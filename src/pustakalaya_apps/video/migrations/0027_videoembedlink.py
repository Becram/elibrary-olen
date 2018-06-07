# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-07 08:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0026_video_submitted_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoEmbedLink',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Updated date')),
                ('video_audio_link_name', models.URLField(max_length=500, verbose_name='Link URL')),
                ('video_audio_link_description', models.TextField(blank=True, max_length=500, verbose_name='Link Description')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.Video', verbose_name='Embed Link')),
            ],
            options={
                'ordering': ['created_date'],
            },
        ),
    ]
