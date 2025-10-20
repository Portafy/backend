"""
WSGI config for Portafy project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'asgi' command.
# This allows the application to use the correct settings based on the environment.
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_ENV", "config.settings.dev")
)

application = get_wsgi_application()
