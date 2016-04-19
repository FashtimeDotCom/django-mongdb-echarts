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
    url(r'^topleft/', outer_dbclass, name="topleft"),
    url(r'^topright/', inner_dbclass, name="topright"),
    url(r'^top_10_industry/', top_10_industry, name="top_10_industry"),
    url(r'^top_10_industry_further/', top_10_industry_further, name="top_10_industry_further"),
    url(r'^one_one/', lefttop, name="lefttop"),
    url(r'^one_two/', righttop, name="righttop"),
    url(r'^fish_bone_disk/', fish_bone_disk, name="fish_bone_disk"),
    url(r'^fish_bone_memory/', fish_bone_memory, name="fish_bone_memory"),
]
