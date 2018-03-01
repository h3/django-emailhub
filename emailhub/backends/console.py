import logging

from django.core.mail.backends.console import EmailBackend as ConsoleEmailBackend  # noqa

from emailhub.utils.email import process_outgoing_email

log = logging.getLogger('emailhub')


class EmailBackend(ConsoleEmailBackend):
    def write_message(self, message):
        process_outgoing_email(message)
        super(EmailBackend, self).write_message(message)
