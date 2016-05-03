# coding:utf8
from .base import *
__author__ = 'kevin'


DEBUG = True

ALLOWED_HOSTS = []


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'


# Application definition

INSTALLED_APPS += [
    'debug_toolbar',
    'home',
    'salt_demo',
]


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
