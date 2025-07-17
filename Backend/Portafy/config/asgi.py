"""
ASGI config for Portafy project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
# Set the default settings module for the 'asgi' command.
# This allows the application to use the correct settings based on the environment.
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_ENV", "config.settings.dev")
)
application = get_asgi_application()
