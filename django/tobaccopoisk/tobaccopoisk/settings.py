"""
Django settings for tobaccopoisk project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
from .private import *
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# * is not safe
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'user_page',
    'auth_page',
    'tobacco_page',
    'about_page',
    'search_page',
    'main_page',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tobaccopoisk.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates') ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tobaccopoisk.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('ru', 'Русский'),
    ('en', 'English'),
)

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

""" Workable for japroc
STATIC_ROOT = '/Users/japro_000/Desktop/TobaccoPoisk/django/tobaccopoisk'
STATICFILES_DIRS = (
    '/Users/japro_000/Desktop/TobaccoPoisk/django/tobaccopoisk/main_page/static',
)
"""

STATIC_URL = '/static/'

#STATIC_ROOT = os.path.normcase(os.path.join(BASE_DIR, "static")) # untrusted definition

STATICFILES_DIRS = (
    os.path.normcase(os.path.join(BASE_DIR, "auth_page/static")),       # untrusted definition
    os.path.normcase(os.path.join(BASE_DIR, "about_page/static")),      # unpizdyasted definition
    os.path.normcase(os.path.join(BASE_DIR, "tobacco_page/static")),    # unhuyasted definition
    os.path.normcase(os.path.join(BASE_DIR, "search_page/static")),     # unjebasted definition
    os.path.normcase(os.path.join(BASE_DIR, "main_page/static")),       # unsisyasted definition
    os.path.normcase(os.path.join(BASE_DIR, "user_page/static")),       # unvyobsted definition
    os.path.normcase(os.path.join(BASE_DIR, "static")),                 # unzhopasted definition
)

SESSION_EXPIRE_AT_BROWSER_CLOSE = False