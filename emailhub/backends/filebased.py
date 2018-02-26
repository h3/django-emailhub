import logging

from django.core.mail.backends.filebased import FileBasedEmailBackend

log = logging.getLogger('emailhub')


class EmailBackend(FileBasedEmailBackend):
    def write_message(self, message):
        log.debug(message)
        super(EmailBackend, self).write_message(message)
