# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-07 08:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('audio', '0026_audio_submitted_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioEmbedLink',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Updated date')),
                ('video_audio_link_name', models.URLField(max_length=500, verbose_name='Embed Link URL')),
                ('video_audio_link_description', models.TextField(blank=True, max_length=500, verbose_name='Embed Link Description')),
                ('audio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audio.Audio', verbose_name='Embed audio Link')),
            ],
            options={
                'ordering': ['created_date'],
            },
        ),
    ]