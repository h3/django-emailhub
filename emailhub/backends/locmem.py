from django.core import mail
from django.core.mail.backends.locmem import LocmemEmailBackend

from emailhub.utils.email import process_outgoing_email


class EmailBackend(LocmemEmailBackend):
    def send_messages(self, messages):
        """Redirect messages to the dummy outbox"""
        msg_count = 0
        for message in messages:  # .message() triggers header validation
            message.message()
            mail.outbox.append(message)
            process_outgoing_email(message)
            msg_count += 1
        return msg_count
