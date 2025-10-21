import environ
from Backend.Portafy.config.settings.dev import FRONTEND_DOMAIN
from .base import *
import os


DEBUG = False
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# Authentication settings
ACCOUNT_EMAIL_VERIFICATION = 'optional'

REST_AUTH["JWT_AUTH_SECURE"] = True

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
FRONTEND_PASSWORD_RESET_URL = os.getenv("FRONTEND_PASSWORD_RESET_URL", "http://localhost:3000/reset_password")
FRONTEND_PAYMENT_SUCCESS_URL = os.getenv("FRONTEND_PAYMENT_SUCCESS_URL", f"{FRONTEND_DOMAIN}/payment-success")

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-qxm$!_4v-vwb)&2cu+fd-*z+c$*_k&p_0ch&mflfv(z7*0#l=v")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "abelmekonen247@gmail.com")
CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY", default="sk_test_xxx")
CHAPA_PUBLIC_KEY = os.getenv("CHAPA_PUBLIC_KEY", default="pk_test_xxx")
SITE_ID = int(os.getenv("SITE_ID", 1))

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://red-d3rb2la4d50c73eg9rsg:6379")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://red-d3rb2la4d50c73eg9rsg:6379") # Optional, for storing task results
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'


env = environ.Env()
env.read_env()

DATABASES = {
    'default': env.db('DATABASE_URL')
}
