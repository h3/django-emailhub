# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from emailhub.utils.audit import AuditableAdminMixin
from emailhub.models import EmailMessage


class EmailMessageAdmin(AuditableAdminMixin, admin.ModelAdmin):
    list_display = ('subject', 'user', 'to_email', 'date_sent',
                    'is_locked', 'is_sent', 'is_error', 'created')
    readonly_fields = ('uuid', 'user', 'date_sent', 'is_sent', 'from_email',
                       'created', 'modified')
    search_fields = ('subject', 'body_text')
    list_filter = (
        'is_sent', 'is_error', 'is_draft', 'is_locked', 'send_error_code')
    date_hierarchy = 'created'
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
                ('created', 'modified', 'date_sent', 'send_retries'),
                'send_error_message',
            )
        }),
    )
admin.site.register(EmailMessage, EmailMessageAdmin)