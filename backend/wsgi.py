"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

env = os.environ.get('ENV')
if env == "prod":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.prod")
if env == "dev":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.base")

application = get_wsgi_application()
