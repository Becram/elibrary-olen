# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-15 11:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('collection', '0001_initial'),
        ('core', '0003_sponsor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Updated date')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Title')),
                ('abstract', models.TextField(verbose_name='Abstract')),
                ('education_level', models.CharField(choices=[('early primary level', 'Early primary level'), ('primary level', 'Primary level'), ('Middle school level', 'Middle school level'), ('highschool level', 'Highschool level'), ('intermediate level', 'Intermediate level')], max_length=255, verbose_name='Education Level')),
                ('category', models.CharField(choices=[('literatures and arts', 'Literature and arts'), ('course materials', 'Course materials'), ('teaching materials', 'Teaching materials'), ('reference materials', 'Reference materials')], max_length=255)),
                ('language', models.CharField(choices=[('nepali', 'Nepali'), ('english', 'English')], max_length=255, verbose_name='Language')),
                ('citation', models.CharField(blank=True, max_length=255, verbose_name='Citation')),
                ('reference_link', models.URLField(blank=True, verbose_name='Reference link')),
                ('additional_note', models.TextField(blank=True, verbose_name='Additional Note')),
                ('description', models.TextField(verbose_name='Description')),
                ('license_type', models.CharField(choices=[('creative commons', 'Creative Commons'), ('copyright retained', 'Copyright retained'), ('apache License 2.0', 'Apache License 2.0'), ('creative commons', 'Creative Commons'), ('mit license', 'MIT License')], max_length=255, verbose_name='License type')),
                ('custom_license', models.TextField(blank=True, verbose_name='Custom license')),
                ('year_of_available', models.DateField(blank=True, verbose_name='Year of available')),
                ('date_of_issue', models.DateField(blank=True, verbose_name='Date of issue')),
                ('place_of_publication', models.CharField(blank=True, max_length=255, verbose_name='Place of publication')),
                ('document_type', models.CharField(choices=[('book', 'Book'), ('working paper', 'Working paper'), ('thesis', 'Thesis'), ('journal paper', 'Journal paper'), ('technical report', 'Technical report'), ('article', 'Article')], max_length=40, verbose_name='Document type')),
                ('document_file_type', models.CharField(choices=[('ppt', 'PPT'), ('doc', 'Doc'), ('docx', 'Docx'), ('pdf', 'PDF'), ('pdf', 'PDF'), ('xlsx', 'Excel'), ('epub', 'Epub'), ('rtf', 'Rtf'), ('mobi', 'Mobi')], max_length=23, verbose_name='Document file type')),
                ('document_interactivity', models.CharField(choices=[('interactive', 'Interactive'), ('noninteractive', 'Non interactive')], max_length=15, verbose_name='Interactive type')),
                ('type', models.CharField(default='document', editable=False, max_length=255)),
                ('document_total_page', models.PositiveIntegerField(verbose_name='Document pages')),
                ('document_identifier_type', models.CharField(choices=[('issn', 'ISSN'), ('ismn', 'ISMN'), ('govt doc', "Gov't Doc"), ('uri', 'URI'), ('isbn', 'ISBN')], max_length=255, verbose_name='Identifier type')),
                ('document_thumbnail', models.ImageField(max_length=255, upload_to='uploads/thumbnails/audio/%Y/%m/%d')),
                ('collection', models.ManyToManyField(to='collection.Collection', verbose_name='Add to these collections')),
                ('document_author', models.ManyToManyField(related_name='authors', to='core.Biography', verbose_name='Document Author')),
                ('document_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Category', verbose_name='Document Category')),
                ('document_editor', models.ManyToManyField(related_name='editors', to='core.Biography', verbose_name='Document Editor')),
                ('document_illustrator', models.ManyToManyField(related_name='illustrators', to='core.Biography', verbose_name='Document Illustrator')),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='DocumentFileUpload',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Updated date')),
                ('file_name', models.CharField(max_length=255, verbose_name='File name')),
                ('upload', models.FileField(max_length=255, upload_to='uploads/documents/%Y/%m/')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document.Document')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DocumentSeries',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Updated date')),
                ('series_name', models.CharField(max_length=255, verbose_name='Series name')),
                ('description', models.TextField(verbose_name='Description')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField()),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='document_series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document.DocumentSeries', verbose_name='Document series'),
        ),
        migrations.AddField(
            model_name='document',
            name='keywords',
            field=models.ManyToManyField(to='core.Keyword', verbose_name='Select list of keywords'),
        ),
        migrations.AddField(
            model_name='document',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Publisher', verbose_name='Publisher name'),
        ),
        migrations.AddField(
            model_name='document',
            name='sponsors',
            field=models.ManyToManyField(to='core.Sponsor', verbose_name='Sponsor'),
        ),
    ]
