from django.core.mail.backends.smtp import DummyEmailBackend


class EmailBackend(DummyEmailBackend):
    """
    Not sure if this backend should generate database entries, for the moment
    I will bet not.
    """
    pass
    # def send_messages(self, email_messages):
    #     for message in email_messages:
    #         process_outgoing_email(message)
    #     super(EmailBackend, self).send_messages(email_messages)
