import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olfati_django.settings')
app = Celery('olfati_django')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = 'redis://:k8fO9PqtglIkXRkW@services.irn9.chabokan.net:48473/0'

app.autodiscover_tasks()
