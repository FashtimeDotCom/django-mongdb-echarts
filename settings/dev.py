# coding:utf8
from .base import *
__author__ = 'kevin'


DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS += [
    'debug_toolbar',
    'home',
]


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
