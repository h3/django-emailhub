# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-01 18:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailhub', '0006_auto_20180301_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailmessage',
            name='to',
            field=models.EmailField(max_length=254, verbose_name='To'),
        ),
    ]
