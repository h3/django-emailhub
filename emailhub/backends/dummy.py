import logging

from django.core.mail.backends.smtp import DummyEmailBackend

log = logging.getLogger('emailhub')


class EmailBackend(DummyEmailBackend):
    pass
    # def send_messages(self, email_messages):
    #     for message in email_messages:
    #         log.debug(message)
    #     super(EmailBackend, self).send_messages(email_messages)
