from datetime import timedelta
from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'accounts',
    'exam',
    "core",
    "litner",
    "markethub",
    "catalog_app.apps.CatalogAppConfig",
    # "django_celery_results",
    "drf_spectacular",
    "storages"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'olfati_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'olfati_django.wsgi.application'

AUTH_USER_MODEL = 'accounts.UserModel'


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# TOKEN.obtain_auth_token
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=90),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
    'ALGORITHM': 'HS256',
}
# تنظیمات JWT
JWT_AUTH = {
    'JWT_GET_USER_SECRET_KEY': None,  # تابع برای دریافت کلید مخفی کاربر (با توجه به شناسه کاربری)
    'JWT_PAYLOAD_HANDLER': 'path.to.custom_payload_handler',  # تابع برای ایجاد بسته داده‌های توکن
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'path.to.custom_response_payload_handler',
    # تابع برای ایجاد پاسخ دریافتی بعد از درخواست توکن
    'ACCESS_TOKEN_LIFETIME': timedelta(weeks=24),  # مدت اعتبار توکن دسترسی
    'REFRESH_TOKEN_LIFETIME': timedelta(weeks=48),  # مدت اعتبار توکن بازیابی
}

REDIRECTURL = "https://olfati.iran.liara.run"
CALLBACKURL = 'https://{REDIRECTURL}/markethub/zarrin-pall/verify/'
MERCHANT = "7bd2714c-3674-4566-a4ff-8ec4ed9fac64"

# مسیر به کلید خصوصی دانلود شده
FIREBASE_ADMIN_KEY_PATH = os.path.join(BASE_DIR, 'firebase_admin_key.json')

# celery settings
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Tehran'

# # CELERY BEAT SCHEDULER
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


AWS_ACCESS_KEY_ID=config("AWS_ACCESS_KEY_ID", cast=str)
AWS_SECRET_ACCESS_KEY=config("AWS_SECRET_ACCESS_KEY", cast=str)
AWS_STORAGE_BUCKET_NAME=config("AWS_STORAGE_BUCKET_NAME", cast=str)
AWS_S3_ENDPOINT_URL=config("AWS_S3_ENDPOINT_URL", cast=str)
AWS_S3_FILE_OVERWRITE=False
AWS_S3_REGION_NAME = 'us-east-1'
