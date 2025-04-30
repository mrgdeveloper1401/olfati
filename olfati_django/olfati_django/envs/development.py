from olfati_django.settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("DEVELOPMENT_SECRET_KEY", cast=str)

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    "debug_toolbar"
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

INTERNAL_IPS = [
    "127.0.0.1",
]

SIMPLE_JWT['SIGNING_KEY'] = SECRET_KEY

JWT_AUTH["JWT_SECRET_KEY"] = SECRET_KEY

CELERY_BROKER_URL = "redis://localhost:6380/2"
CELERY_RESULT_BACKEND = "redis://localhost:6380/3"
