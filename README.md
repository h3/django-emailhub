# PROJECT MOVED: [https://gitlab.com/h3/django-emailhub](https://gitlab.com/h3/django-emailhub)

# django-emailhub

Django-emailhub tries to go a beyond interpolating variable in a template to
send the output by email.

**Note**: Work in progress.


## Installation

Add `multi_email_field` and `emailhub` to your project's settings:

```python
INSTALLED_APPS = [
    'multi_email_field',
    'emailhub',
]
```

**Note**: You don't need to add `multi_email_field` to your requirements,
          emailhub will install it.

Run migrations:

```bash
(venv)$ python manage.py migrate
```

## Python API


```python
from emailhub.utils.email import EmailFromTemplate, send_email

msg = EmailFromTemplate('template-slug-name', lang='en',
                        extra_context={'hello': 'world'}).send_to(user)
```

## Features

### Inboxes

Not actual inboxes, but emails are (optionally) linked to users model.

This makes it possible to build an inbox view for users where they
can see a copy of all emails sent to them.

This is accomplished in two ways, first when using the EmailHub API:


```python
EmailFromTemplate('welcome-message').send_to(user)
```

And when using EmailHub's email backends, it will look for user
emails that matches the destination email and link them.


### Batch sending

Sending email right away is rarely a good idea, having a batch sending 
approach prevents many headaches down the road.

It won't hang your frontend process if the SMTP is slow to respond.

It also allow to have throttling rules to avoid flooing the SMTP.

It also allow to introduce the draft state.


### Draft state

The draft mode works somewhat like standard email draft, but with automated
emails.

When a template email is sent and draft mode is enabled, the email isn't sent
right away. It is only saved in db where it can be edited and sent at a later
time.

This allows to create new email templates and review / correct outgoing emails
before they are actually sent to actual customers.

When the template is stable, draft mode can be disabled and be sent directly.


### Email templates

Email templates are can be defined in the admin. They support:

* translations
* variables (they are actual django templates)
* preset signatures
* overriding default send from email
* allow or block draft mode


### Signature templates

Email templates can (or not) use signature templates defined in the admin.



## Settings


### EMAILHUB\_DEFAULT\_FROM 

If email\_from isn't specified when sending the email or if the template
does not provide a value for it, this setting is used.

```python
EMAILHUB_DEFAULT_FROM = 'no-reply@domain.com'
```


### EMAILHUB\_SEND\_BATCH\_SLEEP 

Sleep N seconds between sending each batches
```python
EMAILHUB_SEND_BATCH_SLEEP = 2
```


### EMAILHUB\_SEND\_BATCH\_SIZE 

Limit the number of Email objects will be sent

```python
EMAILHUB_SEND_BATCH_SIZE = 20
```


### EMAILHUB\_SEND\_MAX\_RETRIES 

Maximum send retries before giving up.

```python
EMAILHUB_SEND_MAX_RETRIES = 3
```


### EMAILHUB\_SEND\_HTML

Send also the HTML version with the text version of the email body (multi-parts)

```python
EMAILHUB_SEND_HTML = True
```


### EMAILHUB\_DRAFT\_MODE

Activate or deactivate draft mode.

```python
EMAILHUB_DRAFT_MODE = True
```


### EMAILHUB\_PRELOADED\_TEMPLATE\_TAGS

These template tags will be preloaded for email templates rendering.

```python
EMAILHUB_PRELOADED_TEMPLATE_TAGS = ['i18n']
```

### EMAILHUB\_TEXT\_TEMPLATE

Template used to render text email templates

```python
EMAILHUB_TEXT_TEMPLATE = """{{% load {template_tags} %}}{content}"""
```

### EMAILHUB\_HTML\_TEMPLATE

Template used to render HTML email templates

```python
EMAILHUB_HTML_TEMPLATE = """
{{% load {template_tags} %}}
{{% language lang|default:"en" %}}
<!DOCTYPE html>
<html lang="{{ lang }}">
  <head><meta charset="utf-8"></head>
  <body>{content}</body>
</html>
"""
```


## Backends

In order to be able to log all outgoing emails, not just those sent from
templates, it is necessary to use EmailHub's email backends.

```python
EMAIL_BACKEND = 'emailhub.backends.smtp.EmailBackend'
```

They are essentially subclasses of the core django email backends.

Here's the conversion table:


| **Django**                                         | **EmailHub**                               |
|----------------------------------------------------|--------------------------------------------|
| `django.core.mail.backends.smtp.EmailBackend`      | `emailhub.backends.smtp.EmailBackend`      |
| `django.core.mail.backends.console.EmailBackend`   | `emailhub.backends.console.EmailBackend`   |
| `django.core.mail.backends.filebased.EmailBackend` | `emailhub.backends.filebased.EmailBackend` |
| `django.core.mail.backends.locmem.EmailBackend`    | `emailhub.backends.locmem.EmailBackend`    |
| `django.core.mail.backends.dummy.EmailBackend`     | `emailhub.backends.dummy.EmailBackend`     |


## Management commands

### emailhub --create-template

```bash
(venv)$ python manage.py emailhub --create-template
```

### emailhub --list-templates

```bash
(venv)$ python manage.py emailhub --list-templates
```

### emailhub --send

Send unsent emails:

```bash
(venv)$ python manage.py emailhub --send
```

### emailhub --status

```bash
(venv)$ python manage.py emailhub --status
```
