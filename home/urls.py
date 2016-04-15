# coding:utf8
from django.conf.urls import url
from .views import *
__author__ = 'kevin'


urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^echarts/$', EchartsIndexView.as_view(), name="echarts"),
    # url(r'^category/$', CategoryListView.as_view(), name="category"),
    # url(r'^attr/', AttrListView.as_view(), name="attr"),
    # url(r'^ci/', CIListView.as_view(), name="ci"),
    # url(r'^ci-add-one-ci/', CIAddOneCIListView.as_view(), name="ci-add-one-ci"),
]

# urlpatterns += [
#     url(r'^getcicategory/', getcicategory, name="getcicategory")
# ]