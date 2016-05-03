# coding:utf8
from .base import *
__author__ = 'kevin'


DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS += [
    'home',
    'salt_demo',
]


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'production.sqlite3'),
    }
}

# python manage.py collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'production_static')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/production_static/'
