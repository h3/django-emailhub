from django.conf import settings

# Default email from
DEFAULT_FROM = getattr(settings, 'EMAILHUB_DEFAULT_FROM', 'no-reply@domain.com')

# Sleep N seconds between sending each batches
SEND_BATCH_SLEEP = getattr(settings, 'EMAILHUB_SEND_BATCH_SLEEP', 2)

# Limit the number of Email objects will be sent
SEND_BATCH_SIZE = getattr(settings, 'EMAILHUB_SEND_BATCH_SIZE', 20)

# Maximum send retries
SEND_MAX_RETRIES = getattr(settings, 'EMAILHUB_SEND_MAX_RETRIES', 3)

# Send also the HTML version (multi-parts)
SEND_HTML = getattr(settings, 'EMAILHUB_SEND_HTML', True)
