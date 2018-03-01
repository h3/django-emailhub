from django.core.mail.backends.filebased import FileBasedEmailBackend

from emailhub.utils.email import process_outgoing_email


class EmailBackend(FileBasedEmailBackend):
    def write_message(self, message):
        process_outgoing_email(message)
        super(EmailBackend, self).write_message(message)
