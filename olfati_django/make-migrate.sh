#!/bin/bash

PATH="/home/debian/django_project/olfati/olfati_django/.venv/bin"

python manage.py makemigrations
python manage.py migrate