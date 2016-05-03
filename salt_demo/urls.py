# coding:utf8
from django.conf.urls import url
from .views import *
__author__ = 'kevin'


urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
]


# AJAX
urlpatterns += [
    url(r'^cmd_run/', cmd_run, name="cmd_run"),
]
