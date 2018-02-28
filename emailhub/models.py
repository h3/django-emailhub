# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
import uuid
import logging

from django.db import models
from django.utils import six
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from emailhub.conf import settings as emailhub_settings
from emailhub.utils.html import icon

log = logging.getLogger('emailhub')
User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


@python_2_unicode_compatible
class EmailMessage(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, blank=True, null=True)
    subject = models.TextField(_('Subject'))
    body_text = models.TextField(_('Body (text)'))
    body_html = models.TextField(_('Body (HTML)'), blank=True, null=True)
    from_email = models.EmailField(_('From'))
    to_email = models.EmailField(_('To'))
    date_created = models.DateTimeField(_('Date created'), auto_now_add=True)
    date_modified = models.DateTimeField(_('Date modified'), auto_now=True)
    date_sent = models.DateTimeField(_('Date sent'), blank=True, null=True)
    is_sent = models.BooleanField(_('Is sent'), default=False, db_index=True)
    is_error = models.BooleanField(_('Is error'), default=False, db_index=True)
    send_retries = models.SmallIntegerField(_('Send retries'), default=0)
    send_error_message = models.TextField(_('Send error message'),
                                          blank=True, null=True)
    send_error_code = models.SmallIntegerField(_('Send error code'),
                                               blank=True, null=True)
    from_template = models.CharField(_('From template'), max_length=100,
                                     blank=True, null=True)
    is_draft = models.BooleanField(
        _('Is draft'), default=False,
        help_text=_("Message marked as draft will not be sent"))
    is_locked = models.BooleanField(
        _('Is locked'), default=False,
        help_text=_("Message marked as locked is being processed"))

    def get_color(self):
        if self.is_error:
            return 'red'
        elif self.is_draft:
            return 'blue'
        elif self.is_locked:
            return 'orange'
        elif self.is_sent:
            return 'green'

    def get_state_label(self):
        if self.is_error:
            return _('Error')
        elif self.is_sent:
            return _('Sent')
        elif self.is_locked:
            return _('Sending')
        elif self.is_draft:
            return _('Draft')

    def get_icon(self):
        i = self.is_draft and 'drafts' or 'email'
        _kwargs = {'tooltip': self.get_state_label(),
                   'css_class': '{}-text'.format(self.get_color())}
        return mark_safe(icon(i, **_kwargs))

    def get_badge(self):
        _tpl = '<span class="badge white-text {color}">{label}</span>'
        _kwargs = {'color': self.get_color(), 'label': self.get_state_label()}
        return mark_safe(_tpl.format(**_kwargs))

    def get_absolute_url(self):
        if not self.customer:
            return reverse('admin:messaging_emailmessage_change',
                           args=[self.pk])
        elif self.is_draft:
            return self.get_change_url()
        else:
            return self.get_detail_url()

    def save(self, *args, **kwargs):
        # force remove new lines & spaces from begining and end of the message
        self.body_text = re.sub('^(\n|\r|\s)+|(\n|\r|\s)+$', '', self.body_text)
        return super(EmailMessage, self).save(*args, **kwargs)

    def __str__(self):
        if self.customer:
            return '"%s" <%s> %s' % (self.customer, self.to_email, self.subject)
        else:
            return '<%s> %s' % (self.to_email, self.subject)

    class Meta:
        verbose_name = _('Email message')
        verbose_name_plural = _('Email messages')
        ordering = ['-date_created', '-date_sent']


@python_2_unicode_compatible
class EmailSignature(models.Model):
    slug = models.SlugField(_('Slug'), max_length=80, blank=False, null=False,
                            unique=False)
    language = models.CharField(_('Language'), max_length=6, default='en',
                                choices=settings.LANGUAGES)
    text_content = models.TextField(_('Text content'))
    html_content = models.TextField(_('HTML content'), blank=True, null=True)

    class Meta:
        verbose_name = _('Email signature')
        verbose_name_plural = _('Email signatures')
        ordering = ['slug']


@python_2_unicode_compatible
class EmailTemplate(models.Model):
    SIGNATURE_CHOICES = (
        ('none', _('No signature')),
        ('default', _('Default')),
    )
    language = models.CharField(_('Language'), max_length=6, default='en',
                                choices=settings.LANGUAGES)
    slug = models.SlugField(_('Slug'), max_length=80, blank=False, null=False,
                            unique=False)
    subject = models.CharField(_('Subject'), max_length=100)
    text_content = models.TextField(_('Text content'))
    html_content = models.TextField(_('HTML content'))
    email_from = models.EmailField(
        _('Email from'), blank=True, null=True,
        help_text=_('Will be sent from "{}" if left blank.').format(
            emailhub_settings.DEFAULT_FROM))
    is_active = models.BooleanField(_('Is active'), default=True)
    is_auto_send = models.BooleanField(
        _('Auto send'), default=False,
        help_text=_('If checked, email will be sent without going through a "draft" state.'))  # noqa
    signature = models.CharField(_('Signature'), max_length=100,
                                 choices=SIGNATURE_CHOICES, default='default')

    def __str__(self):
        return six.text_type('{} ({})'.format(self.subject, self.language))

    class Meta:
        verbose_name = _('Email template')
        verbose_name_plural = _('Email templates')
