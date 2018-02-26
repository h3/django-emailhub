import logging

from django.core.mail.backends.smtp import SMTPEmailBackend

log = logging.getLogger('emailhub')


class EmailBackend(SMTPEmailBackend):
    def _send(self, email_message):
        log.debug(email_message)
        super(EmailBackend, self)._send(email_message)
