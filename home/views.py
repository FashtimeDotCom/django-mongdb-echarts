# coding:utf8
from .models import Db
# Create your views here.
from django.views.generic import TemplateView
import calendar
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse


class IndexView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['asd'] = "123"
        context['current_page'] = "home"
        return context


def utc_to_local(utc_dt):
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)


class EchartsIndexView(TemplateView):
    template_name = "home/echarts.html"
# for poll in Poll.objects(question__startswith="W"):
# print Poll.objects().count()
# for poll in Poll.objects():
#     print poll.question
# print datetime.now().day
print "共{}个".format(Db.objects.count())
# for i in Db.objects(DBId="udb-f22itw"):
#     print utc_to_local(i.CreateTime).weekday()
#     print i.CreateTime
#     print i.CreateTime - timedelta(days=1)
#     print i.CreateTime - timedelta(hours=1)


def field_count(field):
    data = dict()
    data['field_list'] = list(Db.objects.all().distinct(field))
    exec("data['count_list'] = "
         "[Db.objects({}=c).count() for c in data['field_list']]").format(field)
    return data


@csrf_exempt
def lefttop(request):
    # field = request.POST.get('field')
    field = "DBType"
    data = field_count(field)
    data['title'] = field
    data['series_name'] = "数量"
    return JsonResponse(data, safe=False)


@csrf_exempt
def righttop(request):
    # field = request.POST.get('field')
    field = "Role"
    data = field_count(field)
    data['title'] = field
    data['series_name'] = "数量"
    return JsonResponse(data, safe=False)

"""
post = BlogPost.objects(...).only("title", "author.name")
Post.objects(Q(published=True) | Q(publish_date__lte=datetime.now()))
"""
