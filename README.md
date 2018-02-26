# django-emailhub

Django-emailhub tries to go a beyond interpolating variable in a template to
send the output by email.


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


## Backends

In order to be able to log all outgoing emails, not just those sent from
templates, it is necessary to use EmailHub's email backends.

```python
EMAIL_BACKEND = 'emailhub.backends.smtp.EmailBackend'
```

They are essentially subclasses of the core django email backends.

Here's the conversion table:


| **Django**                                       | **EmailHub**                             |
|==================================================|==========================================|
| django.core.mail.backends.smtp.EmailBackend      | emailhub.backends.smtp.EmailBackend      |
| django.core.mail.backends.console.EmailBackend   | emailhub.backends.console.EmailBackend   |
| django.core.mail.backends.filebased.EmailBackend | emailhub.backends.filebased.EmailBackend |
| django.core.mail.backends.locmem.EmailBackend    | emailhub.backends.locmem.EmailBackend    |
| django.core.mail.backends.dummy.EmailBackend     | emailhub.backends.dummy.EmailBackend     |


## Management commands

### emailhub

Send unsent emails:

```bash
(venv)$ python manage.py emailhub --send
```
