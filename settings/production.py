# coding:utf8
from .base import *
__author__ = 'kevin'


DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS += [
    'home',
]


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {}
}
