from .base import *
import os

DEBUG = False
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
ALLOWED_HOSTS = ['yourdomain.com']

# Authentication settings
ACCOUNT_EMAIL_VERIFICATION = 'optional'

REST_AUTH["JWT_AUTH_SECURE"] = True