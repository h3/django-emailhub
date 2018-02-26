import logging

from django.core import mail
from django.core.mail.backends.locmem import LocmemEmailBackend

log = logging.getLogger('emailhub')


class EmailBackend(LocmemEmailBackend):
    def send_messages(self, messages):
        """Redirect messages to the dummy outbox"""
        msg_count = 0
        for message in messages:  # .message() triggers header validation
            log.debug(message)
            message.message()
            mail.outbox.append(message)
            msg_count += 1
        return msg_count
