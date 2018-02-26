# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-26 07:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailhub', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('fr', 'French'), ('en', 'English')], default='en', max_length=6, verbose_name='Language')),
                ('slug', models.SlugField(max_length=80, verbose_name='Slug')),
                ('subject', models.CharField(max_length=100, verbose_name='Subject')),
                ('text_content', models.TextField(verbose_name='Text content')),
                ('html_content', models.TextField(verbose_name='HTML content')),
                ('email_from', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email from')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('is_auto_send', models.BooleanField(default=False, help_text='If checked, email will be sent without going through a "draft" state.', verbose_name='Auto send')),
                ('signature', models.CharField(choices=[('default', 'Default')], default='default', max_length=100, verbose_name='Signature')),
            ],
            options={
                'verbose_name': 'Email template',
                'verbose_name_plural': 'Email templates',
            },
        ),
    ]
