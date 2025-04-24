from olfati_django.settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("PRODUCTION_SECRET_KEY", cast=str)

DATABASES = {
   'default': {
       'ENGINE': "django.db.backends.postgresql",
       'NAME': config("DATABASE_NAME", cast=str),
       'USER': config("DATABASE_USER", cast=str),
       'PASSWORD': config("DATABASE_PASSWORD", cast=str),
       'HOST': config("DATABASE_HOST", cast=str),
       'PORT':  config("DATABASE_PORT", cast=str),
    }
}

ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ["https://cartino-app.ir", 'cartino-app.ir']

# CSRF_TRUSTED_ORIGINS = ["https://cartino.chbk.app"]

CORS_ALLOW_ALL_ORIGINS = True

MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware",)
MIDDLEWARE += [
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
}

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