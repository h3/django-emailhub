# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging

from django.core.management.base import BaseCommand

from emailhub.utils.email import send_unsent_emails

log = logging.getLogger('emailhub')


class Command(BaseCommand):
    """
    EmailHub management command
    """
    help = 'EmailHub management command'

    def add_arguments(self, parser):
        parser.add_argument(
            '--send',
            dest='send',
            action='store_true',
            default=False,
            help='Send unsent emails')

    def handle(self, *args, **options):
        if options.get('send'):
            send_unsent_emails()
