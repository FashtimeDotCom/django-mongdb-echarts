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
    url(r'^outer_group_region/', outer_group_region, name="outer_group_region"),
    url(r'^inner/', inner_dbclass, name="inner"),
    url(r'^top_10_industry_count/', top_10_industry_count, name="top_10_industry_count"),
    url(r'^top_10_industry_count_further/', top_10_industry_count_further, name="top_10_industry_count_further"),
    url(r'^top_10_industry_memory_limit/', top_10_industry_memory_limit, name="top_10_industry_memory_limit"),
    url(r'^top_10_industry_disk_space/', top_10_industry_disk_space, name="top_10_industry_disk_space"),
    url(r'^top_10_company_count/', top_10_company_count, name="top_10_company_count"),
    url(r'^top_10_company_count_further/', top_10_company_count_further, name="top_10_company_count_further"),
    url(r'^top_10_company_memory_limit/', top_10_company_memory_limit, name="top_10_company_memory_limit"),
    url(r'^top_10_company_disk_space/', top_10_company_disk_space, name="top_10_company_disk_space"),
    url(r'^top_10_company_pure_increase_week/', top_10_company_pure_increase_week, name="top_10_company_pure_increase_week"),
    # url(r'^top_10_company_pure_delete_week/', top_10_company_pure_delete_week, name="top_10_company_pure_delete_week"),
    # url(r'^one_one/', lefttop, name="lefttop"),
    # url(r'^one_two/', righttop, name="righttop"),
    url(r'^fish_bone_disk/', fish_bone_disk_by_month, name="fish_bone_disk"),
    url(r'^fish_bone_memory/', fish_bone_memory_by_month, name="fish_bone_memory"),
    url(r'^instance_pure_increase/', instance_pure_increase, name="instance_pure_increase"),
]
