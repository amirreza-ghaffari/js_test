from pathlib import Path
import os
from .local_settings import *


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-o*x@=azva7j_9b&cy9^*xq5@ip%)z=65gf8^7*pjj%8l!n(h&6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'users.CustomUser'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # installed Packages #
    'rest_framework',
    'django_filters',
    'simple_history',
    'drf_yasg',
    'crispy_forms',
    'jdatetime',
    'mattermostdriver',
    'notifications',
    'django_celery_beat',


    # users Module #
    'users',

    # flowchart and diagrams Module #
    'diagram',

    # test Module #
    'flowchart',

    # built_in packages #
    'django.contrib.humanize',

    'index',

]




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # simple history log #

    'simple_history.middleware.HistoryRequestMiddleware',

]

ROOT_URLCONF = 'js_test.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'js_test.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.digikala.com'
EMAIL_HOST_USER = 'Crisis.software@digikala.com'
EMAIL_HOST_PASSWORD = '4AXc@xEbskZRrrF'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

SMS_PANEL_PASSWORD = 'Basic ZGlnaV9IUi9kaWdpa2FsYTpIR1BEU0lOTmxwQXRjeVlL'
MM_USERNAME = 'digikalacrisis.softw'
MM_PASSWORD = '4AXc@xEbskZRrrF'
MM_TOKEN = "wcwz775tpbye7rg9m4cwqtr6ao"
