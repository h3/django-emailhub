# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-01 18:49
from __future__ import unicode_literals

from django.db import migrations
import multi_email_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('emailhub', '0005_auto_20180301_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailmessage',
            name='bcc',
            field=multi_email_field.fields.MultiEmailField(blank=True, null=True, verbose_name='B.C.C.'),
        ),
        migrations.AddField(
            model_name='emailmessage',
            name='cc',
            field=multi_email_field.fields.MultiEmailField(blank=True, null=True, verbose_name='C.C.'),
        ),
        migrations.AddField(
            model_name='emailmessage',
            name='to',
            field=multi_email_field.fields.MultiEmailField(default='test@test.com', verbose_name='To'),
            preserve_default=False,
        ),
    ]
