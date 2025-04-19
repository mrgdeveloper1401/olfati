"""
WSGI config for olfati_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from decouple import config
from django.core.wsgi import get_wsgi_application

debug_mode = config("DEBUG", cast=bool, default=False)

if debug_mode:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olfati_django.envs.development')
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "olfati_django.envs.production")

application = get_wsgi_application()
