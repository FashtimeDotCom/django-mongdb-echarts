# coding:utf8
from django.conf.urls import url
from .views import *
__author__ = 'kevin'


urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
]


# AJAX
urlpatterns += [
    # url(r'^outer/', outer_dbclass, name="outer"),
]
