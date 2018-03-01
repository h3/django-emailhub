# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from emailhub.conf import settings as emailhub_settings
from emailhub.models import EmailMessage, EmailTemplate


class EmailMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'usrs', 'dest', 'date_sent',
                    'is_locked', 'is_sent', 'is_error', 'date_created')
    readonly_fields = ('uuid', 'users', 'date_sent', 'is_sent', 'from_email',
                       'date_created', 'date_modified')
    search_fields = ('subject', 'body_text')
    list_filter = (
        'is_sent', 'is_error', 'is_draft', 'is_locked', 'send_error_code')
    date_hierarchy = 'date_created'
    raw_id_fields = ('users',)
    related_lookup_fields = {
        'fk': ['users'],
    }
    fieldsets = (
        (None, {'fields': (
            ('to', 'from_email'),
            'cc', 'bcc', 'users',
            'subject', 'body_text', 'body_html'
        )}),
        (_('Meta'), {
            'fields': (
                ('uuid', 'is_sent', 'is_draft', 'is_error', 'send_error_code'),
                ('date_created', 'date_modified', 'date_sent', 'send_retries'),
                'send_error_message',
            )
        }),
    )

    def usrs(self, obj):
        return ', '.join(obj.users)

    def dest(self, obj):
        return ', '.join(obj.to)
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
