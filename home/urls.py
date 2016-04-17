# coding:utf8
from django.conf.urls import url
from .views import *
__author__ = 'kevin'


urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^echarts/$', EchartsIndexView.as_view(), name="echarts"),
]


# AJAX
urlpatterns += [
    url(r'^lefttop/', lefttop, name="lefttop"),
    url(r'^righttop/', righttop, name="righttop")
]