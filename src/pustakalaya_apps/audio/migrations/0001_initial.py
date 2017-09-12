# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-09-12 10:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('collection', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Updated date')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Title')),
                ('abstract', models.TextField(verbose_name='Abstract')),
                ('education_label', models.CharField(choices=[('early primary level', 'Early primary level'), ('primary level', 'Primary level'), ('Middle school level', 'Middle school level'), ('highschool level', 'Highschool level'), ('intermediate level', 'Intermediate level')], max_length=255, verbose_name='Education Level')),
                ('category', models.CharField(choices=[('literatures and arts', 'Literature and arts'), ('course materials', 'Course materials'), ('teaching materials', 'Teaching materials'), ('reference materials', 'Reference materials')], max_length=255)),
                ('language', models.CharField(choices=[('nepali', 'Nepali'), ('english', 'English')], max_length=255, verbose_name='Language')),
                ('citation', models.CharField(blank=True, max_length=255, verbose_name='Citation')),
                ('reference_link', models.URLField(blank=True, verbose_name='Reference link')),
                ('additional_note', models.TextField(blank=True, verbose_name='Additional Note')),
                ('sponsor', models.CharField(blank=True, max_length=255, verbose_name='Sponsor')),
                ('description', models.TextField(verbose_name='Description')),
                ('license_type', models.CharField(choices=[('creative commons', 'Creative Commons'), ('copyright retained', 'Copyright retained'), ('apache License 2.0', 'Apache License 2.0'), ('creative commons', 'Creative Commons'), ('mit license', 'MIT License')], max_length=255, verbose_name='License type')),
                ('custom_license', models.TextField(blank=True, verbose_name='Custom license')),
                ('year_of_available', models.DateField(blank=True, verbose_name='Year of available')),
                ('date_of_issue', models.DateField(blank=True, verbose_name='Date of issue')),
                ('place_of_publication', models.CharField(blank=True, max_length=255, verbose_name='Place of publication')),
                ('audio_type', models.CharField(choices=[('audio book', 'Audio Book')], max_length=12, verbose_name='Audio type')),
                ('type', models.CharField(default='audio', editable=False, max_length=255)),
                ('audio_running_time', models.TimeField(verbose_name='Running time')),
                ('audio_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Category', verbose_name='Audio Category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AudioFileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Updated date')),
                ('file_name', models.CharField(max_length=255, verbose_name='File name')),
                ('upload', models.FileField(max_length=255, upload_to='uploads/audio/%Y/%m/')),
                ('audio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audio.Audio')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AudioGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Updated date')),
                ('genre', models.CharField(max_length=255, verbose_name='Genre name')),
                ('genre_description', models.TextField(verbose_name='Genre description')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AudioSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Updated date')),
                ('series_name', models.CharField(max_length=255, verbose_name='Series name')),
                ('description', models.TextField(verbose_name='Description')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='audio',
            name='audio_genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audio.AudioGenre', verbose_name='Audio Genre'),
        ),
        migrations.AddField(
            model_name='audio',
            name='audio_read_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Biography', verbose_name='Read / Voice by'),
        ),
        migrations.AddField(
            model_name='audio',
            name='audio_series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audio.AudioSeries', verbose_name='Audio Series / Volume'),
        ),
        migrations.AddField(
            model_name='audio',
            name='collection',
            field=models.ManyToManyField(to='collection.Collection', verbose_name='Add this audio to these collection'),
        ),
        migrations.AddField(
            model_name='audio',
            name='keywords',
            field=models.ManyToManyField(to='core.Keyword', verbose_name='Select list of keywords'),
        ),
        migrations.AddField(
            model_name='audio',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Publisher', verbose_name='Audio publisher'),
        ),
    ]
