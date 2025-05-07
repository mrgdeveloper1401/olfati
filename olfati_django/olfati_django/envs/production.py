from olfati_django.settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("PRODUCTION_SECRET_KEY", cast=str)

ALLOWED_HOSTS = ''.join(config("PRODUCTION_ALLOWED_HOSTS", cast=list))

# DATABASES = {
#    'default': {
#        'ENGINE': "django.db.backends.postgresql",
#        'NAME': config("DATABASE_NAME", cast=str),
#        'USER': config("DATABASE_USER", cast=str),
#        'PASSWORD': config("DATABASE_PASSWORD", cast=str),
#        'HOST': config("DATABASE_HOST", cast=str),
#        'PORT':  config("DATABASE_PORT", cast=str),
#     }
# }

# docker compose
# DATABASES = {
#    'default': {
#        'ENGINE': "django.db.backends.postgresql",
#        'NAME': config("COMPOSE_POSTGRES_NAME", cast=str),
#        'USER': config("COMPOSE_POSTGRES_USER", cast=str),
#        'PASSWORD': config("COMPOSE_POSTGRES_PASSWORD", cast=str),
#        'HOST': "olfati_postgres",
#        'PORT':  5432
#     }
# }

# docker run system
DATABASES = {
   'default': {
       'ENGINE': "django.db.backends.postgresql",
       'NAME': config("VPS_POSTGRES_NAME", cast=str),
       'USER': config("VPS_POSTGRES_USER", cast=str),
       'PASSWORD': config("VPS_POSTGRES_PASSWORD", cast=str),
       'HOST': config("VPS_POSTGRES_HOST", cast=str),
       'PORT':  config("VPS_POSTGRES_PORT", cast=str)
    }
}

MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware",)
MIDDLEWARE += [
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

CORS_ALLOW_ALL_ORIGINS = True

STORAGES["staticfiles"]["BACKEND"] = "whitenoise.storage.CompressedStaticFilesStorage"

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "SAMEORIGIN"
SECURE_REFERRER_POLICY = "strict-origin"
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SIMPLE_JWT['SIGNING_KEY'] = SECRET_KEY

JWT_AUTH["JWT_SECRET_KEY"] = SECRET_KEY

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },

    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "file_log_prod.log"
        }
    },

    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": False,
        }
    }
}

# use system
CELERY_BROKER_URL = "redis://redis:6380/0"
CELERY_RESULT_BACKEND = "redis://redis:6380/1"

# docker compose
# CELERY_BROKER_URL = "redis://olfati_redis:6379/0"
# CELERY_RESULT_BACKEND = "redis://olfati_redis:6379/1"