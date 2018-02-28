# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from emailhub.conf import settings as emailhub_settings
from emailhub.models import EmailMessage, EmailTemplate


class EmailMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'to_email', 'date_sent',
                    'is_locked', 'is_sent', 'is_error', 'date_created')
    readonly_fields = ('uuid', 'user', 'date_sent', 'is_sent', 'from_email',
                       'date_created', 'date_modified')
    search_fields = ('subject', 'body_text')
    list_filter = (
        'is_sent', 'is_error', 'is_draft', 'is_locked', 'send_error_code')
    date_hierarchy = 'date_created'
    raw_id_fields = ('user',)
    related_lookup_fields = {
        'fk': ['user'],
    }
    fieldsets = (
        (None, {'fields': (
            ('user', 'to_email'),
            'subject', 'body_text', 'body_html'
        )}),
        (_('Meta'), {
            'fields': (
                ('uuid', 'is_sent', 'is_draft', 'is_error', 'send_error_code'),
                ('date_created', 'modified', 'date_sent', 'send_retries'),
                'send_error_message',
            )
        }),
    )
admin.site.register(EmailMessage, EmailMessageAdmin)

if emailhub_settings.DRAFT_MODE is True:
    tpl_list_filter = ('language', 'is_auto_send')
    tpl_list_display = (
        'subject', 'slug', 'language', 'is_active', 'is_auto_send')
    tpl_main_fields = (
        'subject', 'slug', 'email_from', 'language', 'signature',
        'is_auto_send')
else:
    tpl_list_filter = ('language')
    tpl_list_display = (
        'subject', 'slug', 'language', 'is_active')
    tpl_main_fields = (
        'subject', 'slug', 'email_from', 'language', 'signature')


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = tpl_list_display
    list_filter = tpl_list_display
    ordering = ('slug', 'language')
    search_fields = ('slug', 'subject', 'text_content')
    fieldsets = (
        (None, {'fields': tpl_main_fields}),
        (_('Text'), {
            'fields': (
                'text_content',
            )
        }),
        (_('HTML'), {
            'fields': (
                'html_content',
            )
        }),
    )
admin.site.register(EmailTemplate, EmailTemplateAdmin)
