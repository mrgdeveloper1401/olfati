from celery import Celery
import os
from decouple import config

debug_mode = config('DEBUG', default=False, cast=bool)

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'olfati_django.envs.development' if debug_mode else 'olfati_django.envs.production')

app = Celery('olfati_django')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
