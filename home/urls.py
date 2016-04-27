# coding:utf8
from django.conf.urls import url
from .views import *
__author__ = 'kevin'


urlpatterns = [
    # url(r'^$', IndexView.as_view(), name="index"),
    url(r'^$', EchartsIndexView.as_view(), name="echarts"),
    url(r'^echarts/$', EchartsIndexView.as_view(), name="echarts"),
]


# AJAX
urlpatterns += [
    url(r'^outer/', outer_dbclass, name="outer"),
    url(r'^outer_disk_type/', outer_disk_type, name="outer_disk_type"),
    url(r'^inner/', inner_dbclass, name="inner"),
    url(r'^top_10_industry/', top_10_industry, name="top_10_industry"),
    url(r'^top_10_industry_further/', top_10_industry_further, name="top_10_industry_further"),
    url(r'^top_10_company/', top_10_company, name="top_10_company"),
    url(r'^top_10_company_further/', top_10_company_further, name="top_10_company_further"),
    url(r'^one_one/', lefttop, name="lefttop"),
    url(r'^one_two/', righttop, name="righttop"),
    url(r'^fish_bone_disk/', fish_bone_disk_by_month, name="fish_bone_disk"),
    url(r'^fish_bone_memory/', fish_bone_memory_by_month, name="fish_bone_memory"),
    url(r'^instance_pure_increase/', instance_pure_increase, name="instance_pure_increase"),
]
