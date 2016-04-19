# coding:utf8
from .models import Db
# Create your views here.
from django.views.generic import TemplateView
import calendar
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from mongoengine import queryset_manager


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


print "共{}个".format(Db.objects.count())
# print "前十行业列表：{}".format(sorted(Db.outer.order_
# by('DBClass').distinct('Industry'), key=lambda s: Db.outer(Industry=s).count())[-11:-1])
# print Db.outer.distinct('InstanceMode')
for i in Db.objects(ClusterId="udbha-ajv0dp"):
    print i.InstanceMode, i.DBId, i.ClusterId
# print "前十公司列表：{}".format(sorted(Db.outer.distinct('CompanyId'), key=lambda s: Db.outer(CompanyId=s).count())[-11:-1])
# for i in Db.objects.all()[:40]:
#     print i.DBClass, i.DBType
#     print i.CreateTime
#     print i.CreateTime - timedelta(days=1)
#     print i.CreateTime - timedelta(hours=1)


def field_count(field):
    data = dict()
    data['field_list'] = list(Db.objects.all().distinct(field))
    exec("data['count_list'] = "
         "[Db.objects({}=c).count() for c in data['field_list']]").format(field)
    return data

# outer_mysql_ha = Db.objects(InnerMark="No", DBClass="MySQL", InstanceMode="HA")
# outer_mysql_not_ha = Db.objects(InnerMark="No", DBClass="MySQL", InstanceMode="Normal")
# outer_mongo = Db.objects(InnerMark="No", DBClass="MongoDB")
#
# print outer_mysql_ha.count(), outer_mysql_ha.distinct('DBType')
# print outer_mysql_not_ha.count(), outer_mysql_not_ha.distinct('DBType')
# print outer_mongo.count(), outer_mongo.distinct('DBType')


# print Db.objects(DBClass='MongoDB').count()
# print Db.objects(InnerMark='No').count()
# print Db.objects(InnerMark='No', State='Delete').count()
# print Db.objects(InnerMark='No', State='Fail').count()


@csrf_exempt
def outer_dbclass(request):
    data = dict()
    # 图左下角的列表
    data['data'] = Db.outer.order_by('DBClass').distinct('DBType')
    data['data1'] = []
    data['data2'] = []
    data['data3'] = []
    # 获得不同DBClass的所有名字和数量
    # 排序为了保证列表顺序
    for dbclass in Db.outer.order_by('DBClass').distinct('DBClass'):
        data['data1'].append({'value': Db.outer(DBClass=dbclass).count(), 'name': dbclass})

    # 获得区分是否HA的MySQL的所有名字和数量
    # 排序为了保证列表顺序
    for dbclass in Db.outer.order_by('DBClass').distinct('DBClass'):
        if dbclass == 'MySQL':
            for ha in Db.outer(DBClass=dbclass).distinct('InstanceMode'):
                data['data2'].append({'value': Db.outer(DBClass=dbclass, InstanceMode=ha).count(), 'name': ha})
        else:
            data['data2'].append({'value': Db.outer(DBClass=dbclass).count(), 'name': dbclass})

    # 获得区分是否HA、不同版本的DB的所有名字和数量
    # 排序为了保证列表顺序
    for dbclass in Db.outer.order_by('DBClass').distinct('DBClass'):
        if dbclass == 'MySQL':
            for ha in Db.outer(DBClass=dbclass).distinct('InstanceMode'):
                for v in Db.outer(DBClass=dbclass, InstanceMode=ha).distinct('DBType'):
                    data['data3'].append({'value': Db.outer(DBClass=dbclass, InstanceMode=ha, DBType=v).count(), 'name': v})
        else:
            for v in Db.outer(DBClass=dbclass).distinct('DBType'):
                data['data3'].append({'value': Db.outer(DBClass=dbclass, DBType=v).count(), 'name': v})
    return JsonResponse(data, safe=False)


@csrf_exempt
def inner_dbclass(request):
    data = dict()
    # 图左下角的列表
    data['data'] = Db.inner.order_by('DBClass').distinct('DBType')
    data['data1'] = []
    data['data2'] = []
    data['data3'] = []
    # 获得不同DBClass的所有名字和数量
    # 排序为了保证列表顺序
    for dbclass in Db.inner.order_by('DBClass').distinct('DBClass'):
        data['data1'].append({'value': Db.inner(DBClass=dbclass).count(), 'name': dbclass})

    # 获得区分是否HA的MySQL的所有名字和数量
    # 排序为了保证列表顺序
    for dbclass in Db.inner.order_by('DBClass').distinct('DBClass'):
        if dbclass == 'MySQL':
            for ha in Db.inner(DBClass=dbclass).distinct('InstanceMode'):
                data['data2'].append({'value': Db.inner(DBClass=dbclass, InstanceMode=ha).count(), 'name': ha})
        else:
            data['data2'].append({'value': Db.inner(DBClass=dbclass).count(), 'name': dbclass})

    # 获得区分是否HA、不同版本的DB的所有名字和数量
    # 排序为了保证列表顺序
    for dbclass in Db.inner.order_by('DBClass').distinct('DBClass'):
        if dbclass == 'MySQL':
            for ha in Db.inner(DBClass=dbclass).distinct('InstanceMode'):
                for v in Db.inner(DBClass=dbclass, InstanceMode=ha).distinct('DBType'):
                    data['data3'].append({'value': Db.inner(DBClass=dbclass, InstanceMode=ha, DBType=v).count(), 'name': v})
        else:
            for v in Db.inner(DBClass=dbclass).distinct('DBType'):
                data['data3'].append({'value': Db.inner(DBClass=dbclass, DBType=v).count(), 'name': v})
    return JsonResponse(data, safe=False)
"""
Db.inner.order_by('DBClass').distinct('Industry')
sorted(Db.inner.order_by('DBClass').distinct('Industry'), key=lambda s: Db.inner(Industry=s).count())[-11:-1]
"""


@csrf_exempt
def top_10_industry(request):
    top_10_industry_list = sorted(Db.outer.order_by('DBClass').distinct('Industry'), key=lambda s: Db.outer(Industry=s).count())[-11:-1]
    data = dict()
    # 图左下角的列表
    data['data'] = top_10_industry_list
    data['data1'] = []
    data['data2'] = []
    data['data3'] = []
    # 获得不同DBClass的所有名字和数量
    # 排序为了保证列表顺序
    for industry in top_10_industry_list:
        data['data1'].append({'value': Db.outer(Industry=industry).count(), 'name': industry})

    # # 获得区分是否HA的MySQL的所有名字和数量
    # # 排序为了保证列表顺序
    # for dbclass in Db.inner.order_by('DBClass').distinct('DBClass'):
    #     if dbclass == 'MySQL':
    #         for ha in Db.inner(DBClass=dbclass).distinct('InstanceMode'):
    #             data['data2'].append({'value': Db.inner(DBClass=dbclass, InstanceMode=ha).count(), 'name': ha})
    #     else:
    #         data['data2'].append({'value': Db.inner(DBClass=dbclass).count(), 'name': dbclass})
    #
    # # 获得区分是否HA、不同版本的DB的所有名字和数量
    # # 排序为了保证列表顺序
    # for dbclass in Db.inner.order_by('DBClass').distinct('DBClass'):
    #     if dbclass == 'MySQL':
    #         for ha in Db.inner(DBClass=dbclass).distinct('InstanceMode'):
    #             for v in Db.inner(DBClass=dbclass, InstanceMode=ha).distinct('DBType'):
    #                 data['data3'].append({'value': Db.inner(DBClass=dbclass, InstanceMode=ha, DBType=v).count(), 'name': v})
    #     else:
    #         for v in Db.inner(DBClass=dbclass).distinct('DBType'):
    #             data['data3'].append({'value': Db.inner(DBClass=dbclass, DBType=v).count(), 'name': v})
    return JsonResponse(data, safe=False)


@csrf_exempt
def top_10_industry_further(request):
    industry = request.GET['Industry']
    db_version_list = Db.outer(Industry=industry).distinct('DBType')
    db_class_list = Db.outer(Industry=industry).distinct('DBClass')
    data = dict()
    # 图左下角的列表
    data['title'] = u"*{}*DB类型与版本分布".format(industry)
    data['data'] = db_version_list
    data['data1'] = []
    data['data2'] = []
    data['data3'] = []
    # 获得不同DBClass的所有名字和数量
    # 排序为了保证列表顺序
    for db_class in db_class_list:
        data['data1'].append({'value': Db.outer(Industry=industry, DBClass=db_class).count(), 'name': db_class})
    # 获得区分是否HA的MySQL的所有名字和数量
    # 排序为了保证列表顺序
    for dbclass in Db.outer(Industry=industry).order_by('DBClass').distinct('DBClass'):
        if dbclass == 'MySQL':
            for ha in Db.outer(Industry=industry, DBClass=dbclass).distinct('InstanceMode'):
                data['data2'].append({'value': Db.outer(Industry=industry, DBClass=dbclass, InstanceMode=ha).count(), 'name': ha})
        else:
            data['data2'].append({'value': Db.outer(Industry=industry, DBClass=dbclass).count(), 'name': dbclass})

    # 获得区分是否HA、不同版本的DB的所有名字和数量
    # 排序为了保证列表顺序
    for dbclass in Db.outer(Industry=industry).order_by('DBClass').distinct('DBClass'):
        if dbclass == 'MySQL':
            for ha in Db.outer(Industry=industry, DBClass=dbclass).distinct('InstanceMode'):
                for v in Db.outer(Industry=industry, DBClass=dbclass, InstanceMode=ha).distinct('DBType'):
                    data['data3'].append({'value': Db.outer(Industry=industry, DBClass=dbclass, InstanceMode=ha, DBType=v).count(), 'name': v})
        else:
            for v in Db.outer(Industry=industry, DBClass=dbclass).distinct('DBType'):
                data['data3'].append({'value': Db.outer(Industry=industry, DBClass=dbclass, DBType=v).count(), 'name': v})
    return JsonResponse(data, safe=False)


@csrf_exempt
def top_10_company(request):
    top_10_industry_list = sorted(Db.inner.order_by('DBClass').distinct('Industry'), key=lambda s: Db.inner(Industry=s).count())[-11:-1]
    data = dict()
    # 图左下角的列表
    data['data'] = top_10_industry_list
    data['data1'] = []
    data['data2'] = []
    data['data3'] = []
    # 获得不同DBClass的所有名字和数量
    # 排序为了保证列表顺序
    for industry in top_10_industry_list:
        data['data1'].append({'value': Db.outer(Industry=industry).count(), 'name': industry})
    return JsonResponse(data, safe=False)


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
