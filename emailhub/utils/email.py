# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import time
import logging

from smtplib import SMTPDataError
from datetime import datetime

from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage as CreateEmailMessage
from django.contrib.auth import get_user_model
from django.template import Context, Template
from django.utils import six

from emailhub.models import EmailMessage, EmailTemplate
from emailhub.conf import settings as emailhub_settings

log = logging.getLogger('emailhub')
User = get_user_model()


def send_email(msg):
    to = [msg.to]
    kwargs = {'headers': {'X-EmailHub-UUID': msg.uuid}}

    if msg.body_html:
        args = [msg.subject, msg.body_text, msg.from_email, to]
        email = EmailMultiAlternatives(*args, **kwargs)
        email.attach_alternative(msg.body_html, 'text/html')
    else:
        args = [msg.subject, msg.from_email, to]
        email = CreateEmailMessage(*args, **kwargs)

    if msg.is_draft:
        msg.is_draft = False

    if msg.is_error:
        msg.send_retries += 1

    max_retries = emailhub_settings.SEND_MAX_RETRIES
    if msg.send_retries > max_retries:
        msg.is_error = True
        msg.is_sent = False
        msg.send_error_message = 'Max retries reached ({})'.format(max_retries)
        log.debug('Not seding email (max retry of {} reached)'.format(
            emailhub_settings.SEND_MAX_RETRIES))
    else:
        email.debug = True
        try:
            email.send()
            msg.is_error = False
            msg.is_sent = True
            msg.date_sent = datetime.now()
            log.debug('EMAIL SENT > "{}" to {}'.format(
                six.text_type(msg.subject), msg.to))
        except SMTPDataError as e:
            code, error = e
            msg.send_error_code = e.smtp_code
            msg.send_error_message = e.smtp_error
            msg.is_error = True
            msg.is_sent = False
            msg.date_sent = None
            log.debug('EMAIL SMTP ERROR > "{}" to {} ({})'.format(
                six.text_type(msg.subject), msg.to, msg))
            log.error(six.text_type(e))
        except Exception as e:
            msg.send_error_message = e.message
            msg.is_error = True
            msg.is_sent = False
            msg.date_sent = None
            log.debug('EMAIL ERROR > "{}" to {} ({})'.format(
                six.text_type(msg.subject), msg.to, msg))
            log.error(six.text_type(e))
    msg.save()
    return msg


def send_unsent_emails():
    log.debug('Sending unsent emails')
    unsent_emails = EmailMessage.objects.filter(
        is_sent=False, is_draft=False, is_locked=False,
        send_retries__lte=emailhub_settings.SEND_MAX_RETRIES
    )[:emailhub_settings.SEND_BATCH_SIZE]
    unset_email_ids = [unsent_email.id for unsent_email in unsent_emails]
    EmailMessage.objects.filter(id__in=unset_email_ids).update(is_locked=True)
    batch = 0
    for msg in unsent_emails:
        batch += 1
        # flood control
        if batch == emailhub_settings.SEND_BATCH_SIZE:
            log.debug('Sleeping for {} seconds'.format(
                emailhub_settings.SEND_BATCH_SLEEP))
            batch = 0
            time.sleep(emailhub_settings.SEND_BATCH_SLEEP)
        send_email(msg)
    EmailMessage.objects.filter(id__in=unset_email_ids).update(is_locked=False)


class EmailFromTemplate(object):
    slug = None
    extra_context = None
    user = None

    def __init__(self, slug, extra_context=None, lang=None, is_draft=True):
        self.slug = slug
        self.language = lang
        self.is_draft = is_draft
        self.extra_context = extra_context

    def get_template(self):
        kw = {'slug': self.slug}
        if hasattr(self, 'user'):
            kw['language'] = self.language
        try:
            tpl = EmailTemplate.objects.get(**kw)
        except EmailTemplate.DoesNotExist:
            tpl = None
        except EmailTemplate.MultipleObjectsReturned:
            log.error('Multiple templates returned for {}, using first object. THIS IS A CONFIGURATION ERROR.'.format(kw))  # noqa
            tpl = EmailTemplate.objects.filter(**kw).first()
        return tpl

    def _force_i18n(self, i):
        """
        fix because we have no request context, so date templatetags cannot
        determine the correct language
        """
        return '{% load i18n %}{% language lang|default:"fr" %}' + \
               i + '{% endlanguage %}'

    def _i18n_template(self, path):
        return get_template(path)

    def get_context(self):
        context = {
            'email': {},
            # 'base_url': settings.BASE_URL,
            'lang': self.language,
        }

        if hasattr(self, 'user'):
            context.update({'user': self.user})
        if self.extra_context:
            context.update(self.extra_context)
        return context

    def render(self, content, context):
        try:
            return Template(self._force_i18n(content)).render(Context(context))
        except Exception as e:
            log.exception('Exception while rendering template {}: {}'.format(
                self.slug, e))
            return ''

    def send_to(self, user, force=True):
        """
        This method does not actually send any email, it just create the message
        object in the database. A cron process then send message flagged
        is_sent=False at regular interval.
        """
        self.user = user
        if self.language is None:
            # TODO: this is wrong assumption
            self.language = self.user.userprofile.language
        tpl = self.get_template()
        if tpl is None:
            log.critical(
                'COULD NOT CREATE EMAIL: Missing %s email template for %s' % (
                    dict(settings.LANGUAGES).get(self.language), self.slug))
        else:
            send_from = tpl.email_from or emailhub_settings.DEFAULT_FROM
            ctx = self.get_context()
            ctx.update({
                'signature': tpl.signature
            })
            kw = {
                'from_email': send_from,
                'to': self.user.email,
                'subject': tpl.subject,
            }
            tags = ' '.join(emailhub_settings.PRELOADED_TEMPLATE_TAGS)
            if tpl.text_content:
                kw['body_text'] = emailhub_settings.TEXT_TEMPLATE.format(
                    content=self.render(tpl.text_content, ctx),
                    template_tags=tags)
            if tpl.text_content:
                kw['body_html'] = emailhub_settings.HTML_TEMPLATE.format(
                    content=self.render(tpl.html_content, ctx),
                    template_tags=tags)

            msg = EmailMessage(**kw)
            msg.from_template = self.slug
            msg.is_draft = self.is_draft
            if tpl.is_auto_send:
                msg.is_draft = False
            msg.save()
            msg.users.add(self.user)

            # Email are now sent with a cron job
            # if not self.is_draft and force:
            #     send_email(msg)

            return msg


class SystemEmailFromTemplate(EmailFromTemplate):
    slug = None
    extra_context = None
    user = None

    def __init__(self, slug, extra_context=None):
        # self.company = get_current_company()
        self.slug = slug
        self.language = self.company.notification_language
        self.extra_context = extra_context or {}

    def get_template(self):
        kw = {'slug': self.slug}
        kw['language'] = self.language
        try:
            tpl = EmailTemplate.objects.get(**kw)
        except EmailTemplate.DoesNotExist:
            tpl = None
        except EmailTemplate.MultipleObjectsReturned:
            log.error('Multiple templates returned for {}, using first object. THIS IS A CONFIGURATION ERROR.'.format(kw))  # noqa
            tpl = EmailTemplate.objects.filter(**kw).first()
        return tpl

    def send(self, actor='system', force=True, to_email=None, lang=None):
        """
        This method does not actually send any email, it just create the message
        object in the database. A cron process then send message flagged
        is_sent=False at regular interval.
        """
        if lang:
            self.language = lang
        ctx = self.get_context()
        tpl = self.get_template()
        to_email = to_email or self.company.notification_email
        if not to_email:
            log.debug('No notification email set, not sending any notification')
        elif tpl is None:
            log.critical(
                'COULD NOT CREATE EMAIL: Missing %s email template for %s' % (
                    dict(settings.LANGUAGES).get(self.language), self.slug))
        else:
            kw = {
                'from_email': emailhub_settings.DEFAULT_FROM,
                'to_email': to_email,
                'is_sent': False,
                'is_error': False,
                'subject': tpl.subject,
            }
            if tpl.text_content:
                kw['body_text'] = self.render(tpl.text_content, ctx)
            if tpl.text_content:
                kw['body_html'] = self.render(tpl.html_content, ctx)

            msg = EmailMessage(**kw)
            msg.from_template = self.slug
            if tpl.is_auto_send:
                msg.is_draft = False
            msg.save()

            send_email(msg)
            return msg


def get_template_choices(lang):

    qs = EmailTemplate.objects.filter(language=lang)
    values_dict = qs.values('slug', 'subject')
    unique_slugs = set()
    unique_choices = []

    for v in values_dict:
        if v['slug'] not in unique_slugs:
            unique_choices.append((v['slug'], v['subject']))
            unique_slugs.add(v['slug'])

    return unique_choices


def process_outgoing_email(message):
    if 'X-EmailHub-UUID' not in message.extra_headers.keys():
        for to in message.to:
            kw = {
                'to': to,
                'from_email': message.from_email,
                'subject': message.subject,
                'body_text': message.body,
                'is_draft': False,
                'is_sent': True,
            }
            if len(message.alternatives) and len(message.alternatives[0]):
                kw['body_html'] = message.alternatives[0][0]

            msg = EmailMessage(**kw)
            msg.save()
            dests = User.objects.filter(
                email__in=message.recipients())
            if dests.count():
                for user in dests:
                    msg.users.add(user)
