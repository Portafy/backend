from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
app = Celery('Portafy')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()