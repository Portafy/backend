from .base import *
import os

DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = []

FRONTEND_DOMAIN = os.getenv("FRONTEND_DOMAIN", "http://localhost:3000")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
FRONTEND_PASSWORD_RESET_URL = os.getenv("FRONTEND_PASSWORD_RESET_URL", "http://localhost:3000/reset_password")
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-qxm$!_4v-vwb)&2cu+fd-*z+c$*_k&p_0ch&mflfv(z7*0#l=v")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "abelmekonen247@gmail.com")
CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY", default="sk_test_xxx")
CHAPA_PUBLIC_KEY = os.getenv("CHAPA_PUBLIC_KEY", default="pk_test_xxx")
SITE_ID = int(os.getenv("SITE_ID", 1))

FRONTEND_PAYMENT_SUCCESS_URL = os.getenv("FRONTEND_PAYMENT_SUCCESS_URL", f"{FRONTEND_DOMAIN}/payment-success")

INSTALLED_APPS += [
    "debug_toolbar",
]

# ------------------------------
# CORS
# ------------------------------
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

ACCOUNT_EMAIL_VERIFICATION = 'none'

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0' # Optional, for storing task results
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'