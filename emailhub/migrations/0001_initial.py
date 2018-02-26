# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-26 05:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('subject', models.TextField(verbose_name='Subject')),
                ('body_text', models.TextField(verbose_name='Body (text)')),
                ('body_html', models.TextField(verbose_name='Body (html)')),
                ('from_email', models.EmailField(max_length=254, verbose_name='From')),
                ('to_email', models.EmailField(max_length=254, verbose_name='To')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Date modified')),
                ('date_sent', models.DateTimeField(blank=True, null=True, verbose_name='Date sent')),
                ('is_sent', models.BooleanField(db_index=True, default=False, verbose_name='Is sent')),
                ('is_error', models.BooleanField(db_index=True, default=False, verbose_name='Is error')),
                ('send_retries', models.SmallIntegerField(default=0, verbose_name='Send retries')),
                ('send_error_message', models.TextField(blank=True, null=True, verbose_name='Send error message')),
                ('send_error_code', models.SmallIntegerField(blank=True, null=True, verbose_name='Send error code')),
                ('from_template', models.CharField(blank=True, max_length=100, null=True, verbose_name='From template')),
                ('is_draft', models.BooleanField(default=False, help_text='Message marked as draft will not be sent', verbose_name='Is draft')),
                ('is_locked', models.BooleanField(default=False, help_text='Message marked as locked is being processed', verbose_name='Is locked')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_created', '-date_sent'],
                'verbose_name': 'Email message',
                'verbose_name_plural': 'Email messages',
            },
        ),
    ]
