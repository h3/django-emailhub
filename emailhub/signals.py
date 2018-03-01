import django.dispatch

on_email_out = django.dispatch.Signal(providing_args=["email"])
