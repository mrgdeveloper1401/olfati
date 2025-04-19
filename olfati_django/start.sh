#!/bin/sh

python manage.py collectstatic --noinput
gunicorn olfati_django.wsgi -b 0.0.0.0:8000