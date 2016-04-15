# coding:utf8
from .models import Poll, Db
# Create your views here.
from django.views.generic import TemplateView
from datetime import datetime


class IndexView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['asd'] = "123"
        context['current_page'] = "home"
        return context


class EchartsIndexView(TemplateView):
    template_name = "home/echarts.html"
# for poll in Poll.objects(question__startswith="W"):
# print Poll.objects().count()
# for poll in Poll.objects():
#     print poll.question
# print datetime.now().day
print "共{}个".format(Db.objects.count())

# queryset没有属性
# for i in Db.objects[:1]:
#     print i
# for f in Db.objects():
#     print f.to_json(), f.ModifyTime.day == datetime.now().day
# Db(DBId='1', InstanceMode="2", ModifyTime=datetime.now()).save()
# Db.objects(DBId=None).delete()
