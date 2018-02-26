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
        parser.add_argument(
            '--status',
            dest='status',
            action='store_true',
            default=False,
            help='EmailHub system status')
        parser.add_argument(
            '--create-template',
            dest='create_template',
            action='store_true',
            default=False,
            help='Create a new template')
        parser.add_argument(
            '--list-templates',
            dest='list_templates',
            action='store_true',
            default=False,
            help='List templates')

    def handle(self, *args, **options):
        if options.get('send'):
            send_unsent_emails()
