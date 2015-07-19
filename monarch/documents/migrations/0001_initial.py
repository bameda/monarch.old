# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import monarch.documents.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=256, verbose_name='subject')),
                ('author', models.CharField(max_length=256, verbose_name='author')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('last_modified_date', models.DateTimeField(auto_now=True, verbose_name='last modified date')),
                ('description', models.TextField(blank=True, null=True, verbose_name='sdescription')),
                ('file', models.FileField(upload_to=monarch.documents.models.calculate_document_path, verbose_name='file')),
            ],
            options={
                'verbose_name_plural': 'documents',
                'verbose_name': 'document',
            },
        ),
    ]
