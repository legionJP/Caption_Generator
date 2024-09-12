from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from kombu import Exchange, Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vuploader.settings')

app = Celery('vuploader')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

CELERY_BROKER_TRANSPORT_OPTIONS = {
    'visibility_timeout': 3600, #1hr
    'retry_pocily': {
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.5,
    }
}