import os
from pathlib import Path

import environ
from dj_database_url import parse as db_url

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Default values
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["127.0.0.1"]),
    DBBACKUP_STORAGE_OPTIONS=(dict, {'location': 'backup/'}),
    SECRET_KEY=(str, "kjfdlskfjadsklůfhoajfkl55Z656W554534534dkfjdsklf"),
    CSRF_TRUSTED_ORIGINS=(list, ['https://*.cechpetr.cz', 'http://*.cechpetr.cz',]),
    ENVIRONMENT=(str, "localhost"),
    EMAIL_HOST=(str, 'EMAIL_HOST'),
    EMAIL_HOST_USER=(str, "EMAIL_HOST_USER"),
    EMAIL_HOST_PASSWORD=(str, "EMAIL_HOST_PASSWORD"),
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '../.env'))

# Configurable by env
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS')
DBBACKUP_STORAGE_OPTIONS = env.dict("DBBACKUP_STORAGE_OPTIONS")
DATABASES = {
        'default': env.db_url(
            'DATABASE_URL',
            default='postgres://postgres:postgres@127.0.0.1:5432/kontraktor',
        )
    }
# CACHES = {
#     'redis': env.cache_url('REDIS_URL')
# }


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "django_extensions",
    "betterforms",
    "weasyprint",
    "django_filters",
    "django_tables2",
    "crispy_forms",
    "crispy_bootstrap5",
    "dbbackup",
    "easy_pdf",

    "authentication",
    "attachments",
    "clients",
    "contracts",
    "emailing",
    "operators",
    "proposals",

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

ROOT_URLCONF = 'kontraktor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.media",
            ],
        },
    },
]

WSGI_APPLICATION = 'kontraktor.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'cs'

TIME_ZONE = 'Europe/Prague'

USE_I18N = True

USE_L10N = True

USE_TZ = False

USE_THOUSAND_SEPARATOR = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'staticfiles/'),
#
# ]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SHELL_PLUS = "ipython"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_URL = "/authentication/login"

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'

sentry_sdk.init(
    dsn="https://9ea84b5992f44eda9cac15876c116655@o4505028506353664.ingest.sentry.io/4505028521689088",
    integrations=[
        DjangoIntegration(),
    ],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    environment=env("ENVIRONMENT")
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

# EMAIL_HOST = 'smtp.forpsi.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = "kontraktor@cechpetr.cz"
# EMAIL_HOST_PASSWORD = "yPI38^7rG7&9"
# DEFAULT_FROM_EMAIL = "kontraktor@cechpetr.cz"
