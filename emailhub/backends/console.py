import logging

from django.core.mail.backends.console import ConsoleEmailBackend

log = logging.getLogger('emailhub')


class EmailBackend(ConsoleEmailBackend):
    def write_message(self, message):
        log.debug(message)
        super(EmailBackend, self).write_message(message)
