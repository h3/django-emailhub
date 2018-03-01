from django.core.mail.backends.smtp import SMTPEmailBackend

from emailhub.utils.email import process_outgoing_email


class EmailBackend(SMTPEmailBackend):
    def _send(self, message):
        process_outgoing_email(message)
        super(EmailBackend, self)._send(message)
