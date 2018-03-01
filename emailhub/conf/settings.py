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

# Send also the HTML version (multi-parts)
DRAFT_MODE = getattr(settings, 'EMAILHUB_DRAFT_MODE', True)

# Template tags specified here will be loaded for all text and html templates
PRELOADED_TEMPLATE_TAGS = getattr(
    settings, 'EMAILHUB_PRELOADED_TEMPLATE_TAGS', ['i18n'])

# Template string used to render text email
TEXT_TEMPLATE = getattr(
    settings, 'EMAILHUB_TEXT_TEMPLATE',
    """{{% load {template_tags} %}}{content}""")

# Template string used to render HTML email
HTML_TEMPLATE = getattr(
    settings, 'EMAILHUB_HTML_TEMPLATE',
    """
{{% load {template_tags} %}}
{{% language lang|default:"en" %}}
<!DOCTYPE html>
<html lang="{{ lang }}">
  <head><meta charset="utf-8"></head>
  <body>{content}</body>
</html>
""")
