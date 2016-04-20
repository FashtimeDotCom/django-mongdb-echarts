# coding:utf8
from .models import Db, Db_HA
# Create your views here.
from django.views.generic import TemplateView
import calendar
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
import pytz
import datetime
from udbshow.settings import TIME_ZONE
from operator import itemgetter


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
    local_dt = datetime.datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)


def local_to_utc(local_dt, time_zone):
    local = pytz.timezone(time_zone)
    local_dt = local.localize(local_dt, is_dst=None)
    return local_dt.astimezone(pytz.utc)


class EchartsIndexView(TemplateView):
    template_name = "home/echarts.html"


print "共{}个".format(Db.objects.count())
print "HA共{}个".format(Db_HA.objects.count())
# print "前十行业列表：{}".format(sorted(Db.outer.order_
# by('DBClass').distinct('Industry'), key=lambda s: Db.outer(Industry=s).count())[-11:-1])
# print Db.outer.distinct('InstanceMode')
# for i in Db.objects(ClusterId="udbha-ajv0dp"):
#     print i.InstanceMode, i.DBId, i.ClusterId
# print "前十公司列表：{}".format(sorted(Db.outer.distinct('CompanyId'), key=lambda s: Db.outer(CompanyId=s).count())[-10:])


def field_count(field):
    data = dict()
    data['field_list'] = list(Db.objects.all().distinct(field))
    exec("data['count_list'] = "
         "[Db.objects({}=c).count() for c in data['field_list']]").format(field)
    return data


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
            # 非HA
            data['data2'].append({'value': Db.outer(DBClass=dbclass, ClusterId='').count(), 'name': 'Nomal'})
            # HA
            data['data2'].append({'value': Db.outer(DBClass=dbclass, ClusterId__ne='').count(), 'name': 'HA'})
            # for ha in Db.outer(DBClass=dbclass).distinct('InstanceMode'):
            #     data['data2'].append({'value': Db.outer(DBClass=dbclass, InstanceMode=ha).count(), 'name': ha})
        else:
            data['data2'].append({'value': Db.outer(DBClass=dbclass).count(), 'name': dbclass})

    # 获得区分是否HA、不同版本的DB的所有名字和数量
    # 排序为了保证列表顺序
    for dbclass in Db.outer.order_by('DBClass').distinct('DBClass'):
        if dbclass == 'MySQL':
            # 非HA
            for v in Db.outer(DBClass=dbclass, ClusterId='').distinct('DBType'):
                data['data3'].append({'value': Db.outer(DBClass=dbclass, ClusterId='', DBType=v).count(), 'name': v})
            # HA
            for v in Db.outer(DBClass=dbclass, ClusterId__ne='').distinct('DBType'):
                data['data3'].append({'value': Db.outer(DBClass=dbclass, ClusterId__ne='', DBType=v).count(), 'name': v})
            # for ha in Db.outer(DBClass=dbclass).distinct('InstanceMode'):
            #     for v in Db.outer(DBClass=dbclass, InstanceMode=ha).distinct('DBType'):
            #         data['data3'].append({'value': Db.outer(DBClass=dbclass, InstanceMode=ha, DBType=v).count(), 'name': v})
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
            # 非HA
            data['data2'].append({'value': Db.inner(DBClass=dbclass, ClusterId='').count(), 'name': 'Nomal'})
            # HA
            data['data2'].append({'value': Db.inner(DBClass=dbclass, ClusterId__ne='').count(), 'name': 'HA'})
            # for ha in Db.inner(DBClass=dbclass).distinct('InstanceMode'):
            #     data['data2'].append({'value': Db.inner(DBClass=dbclass, InstanceMode=ha).count(), 'name': ha})
        else:
            data['data2'].append({'value': Db.inner(DBClass=dbclass).count(), 'name': dbclass})

    # 获得区分是否HA、不同版本的DB的所有名字和数量
    # 排序为了保证列表顺序
    for dbclass in Db.inner.order_by('DBClass').distinct('DBClass'):
        if dbclass == 'MySQL':
            # 非HA
            for v in Db.inner(DBClass=dbclass, ClusterId='').distinct('DBType'):
                data['data3'].append({'value': Db.inner(DBClass=dbclass, ClusterId='', DBType=v).count(), 'name': v})
            # HA
            for v in Db.inner(DBClass=dbclass, ClusterId__ne='').distinct('DBType'):
                data['data3'].append({'value': Db.inner(DBClass=dbclass, ClusterId__ne='', DBType=v).count(), 'name': v})
            # for ha in Db.inner(DBClass=dbclass).distinct('InstanceMode'):
            #     for v in Db.inner(DBClass=dbclass, InstanceMode=ha).distinct('DBType'):
            #         data['data3'].append({'value': Db.inner(DBClass=dbclass, InstanceMode=ha, DBType=v).count(), 'name': v})
        else:
            for v in Db.inner(DBClass=dbclass).distinct('DBType'):
                data['data3'].append({'value': Db.inner(DBClass=dbclass, DBType=v).count(), 'name': v})
    return JsonResponse(data, safe=False)


@csrf_exempt
def top_10_industry(request):
    data = {
        'data': [],
        'data1': []
    }
    top_10_industry_tuple = []
    industries = Db.outer.item_frequencies('Industry', normalize=True)
    top_industries = sorted(industries.items(), key=itemgetter(1), reverse=True)[:10]
    for t, f in top_industries:
        top_10_industry_tuple.append((t, Db.outer(Industry=t).count()))
    # 图左下角的列表
    data['data'] = [i for i, j in top_10_industry_tuple]
    # 获得不同DBClass的所有名字和数量
    # 排序为了保证列表顺序
    for industry, count in top_10_industry_tuple:
        data['data1'].append({'value': count, 'name': industry})
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
            # 非HA
            _no_ha_count = Db.outer(Industry=industry, DBClass=dbclass, ClusterId='').count()
            if _no_ha_count:
                data['data2'].append({'value': _no_ha_count, 'name': 'Nomal'})
            # HA
            _ha_count = Db.outer(Industry=industry, DBClass=dbclass, ClusterId__ne='').count()
            if _ha_count:
                data['data2'].append({'value': Db.outer(Industry=industry, DBClass=dbclass, ClusterId__ne='').count(), 'name': 'HA'})
        else:
            data['data2'].append({'value': Db.outer(Industry=industry, DBClass=dbclass).count(), 'name': dbclass})

    # 获得区分是否HA、不同版本的DB的所有名字和数量
    # 排序为了保证列表顺序
    for dbclass in Db.outer(Industry=industry).order_by('DBClass').distinct('DBClass'):
        if dbclass == 'MySQL':
            # 非HA
            for v in Db.outer(Industry=industry, DBClass=dbclass, ClusterId='').distinct('DBType'):
                data['data3'].append({'value': Db.outer(Industry=industry, DBClass=dbclass, ClusterId='', DBType=v).count(), 'name': v})
            # HA
            for v in Db.outer(Industry=industry, DBClass=dbclass, ClusterId__ne='').distinct('DBType'):
                data['data3'].append({'value': Db.outer(Industry=industry, DBClass=dbclass, ClusterId__ne='', DBType=v).count(), 'name': v})
        else:
            for v in Db.outer(Industry=industry, DBClass=dbclass).distinct('DBType'):
                data['data3'].append({'value': Db.outer(Industry=industry, DBClass=dbclass, DBType=v).count(), 'name': v})
    return JsonResponse(data, safe=False)


@csrf_exempt
def top_10_company(request):
    data = {
        'category': [],
        'data1': [],
    }
    top_10_company_list = []
    companies = Db.outer.item_frequencies('CompanyName', normalize=True)
    top_companies = sorted(companies.items(), key=itemgetter(1), reverse=True)[:10]
    for t, f in top_companies:
        top_10_company_list.append((t, Db.outer(CompanyName=t).count()))
    # 图左下角的列表
    data['category'] = [i for i, j in top_10_company_list]
    for company, count in top_10_company_list:
        data['data1'].append({'value': count, 'name': company})
    return JsonResponse(data, safe=False)


@csrf_exempt
def top_10_company_further(request):
    company = request.GET['CompanyName']
    db_version_list = Db.outer(CompanyName=company).distinct('DBType')
    db_class_list = Db.outer(CompanyName=company).distinct('DBClass')
    data = {

        'title': u"*{}*DB类型与版本分布".format(company),
        'category': db_version_list,
        'data1': [],
        'data2': [],
        'data3': [],
    }
    # DBClass
    for db_class in db_class_list:
        data['data1'].append({'value': Db.outer(CompanyName=company, DBClass=db_class).count(), 'name': db_class})
    # 是否HA
    for dbclass in Db.outer(CompanyName=company).order_by('DBClass').distinct('DBClass'):
        if dbclass == 'MySQL':
            # 非HA
            _no_ha_count = Db.outer(CompanyName=company, DBClass=dbclass, ClusterId='').count()
            if _no_ha_count:
                data['data2'].append({'value': _no_ha_count, 'name': 'Nomal'})
            # HA
            _ha_count = Db.outer(CompanyName=company, DBClass=dbclass, ClusterId__ne='').count()
            if _ha_count:
                data['data2'].append({'value': Db.outer(CompanyName=company, DBClass=dbclass, ClusterId__ne='').count(), 'name': 'HA'})
        else:
            data['data2'].append({'value': Db.outer(CompanyName=company, DBClass=dbclass).count(), 'name': dbclass})

    for dbclass in Db.outer(CompanyName=company).order_by('DBClass').distinct('DBClass'):
        if dbclass == 'MySQL':
            # 非HA
            for v in Db.outer(CompanyName=company, DBClass=dbclass, ClusterId='').distinct('DBType'):
                data['data3'].append({'value': Db.outer(CompanyName=company, DBClass=dbclass, ClusterId='', DBType=v).count(), 'name': v})
            # HA
            for v in Db.outer(CompanyName=company, DBClass=dbclass, ClusterId__ne='').distinct('DBType'):
                data['data3'].append({'value': Db.outer(CompanyName=company, DBClass=dbclass, ClusterId__ne='', DBType=v).count(), 'name': v})
        else:
            for v in Db.outer(CompanyName=company, DBClass=dbclass).distinct('DBType'):
                data['data3'].append({'value': Db.outer(CompanyName=company, DBClass=dbclass, DBType=v).count(), 'name': v})
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
    field = "State"
    data = field_count(field)
    data['title'] = field
    data['series_name'] = "数量"
    return JsonResponse(data, safe=False)


def fish_bone_disk_by_month(request):
    data = dict()
    data['title'] = 'disk space净新增(GB)'
    data['data1'] = []
    data['data2'] = []
    data['data3'] = []
    _utc_now = local_to_utc(datetime.datetime.now(), TIME_ZONE)
    seven_month_list = [month for month in range(_utc_now.month - 5, _utc_now.month+1) if month > 0]
    data['y'] = ["{}月".format(_i) for _i in seven_month_list]
    for month in seven_month_list:
        data['data1'].append(Db.outer_with_delete_and_fail(CreateMonth=month).sum('DiskSpace'))
        data['data2'].append(0 - Db.outer_with_delete_and_fail(ModifyMonth=month, State="Delete").sum('DiskSpace'))
    for _i in xrange(0, len(seven_month_list)):
        data['data3'].append(data['data1'][_i] + data['data2'][_i])
    return JsonResponse(data, safe=False)


def fish_bone_memory_by_month(request):
    data = {
        'title': 'memory limit净新增(MB)',
        'data1': [],
        'data2': [],
        'data3': [],
    }
    _utc_now = local_to_utc(datetime.datetime.now(), TIME_ZONE)
    seven_month_list = [month for month in range(_utc_now.month - 5, _utc_now.month+1) if month > 0]
    data['y'] = ["{}月".format(_i) for _i in seven_month_list]
    for month in seven_month_list:
        data['data1'].append(Db.outer_with_delete_and_fail(CreateMonth=month).sum('MemoryLimit'))
        data['data2'].append(0 - Db.outer_with_delete_and_fail(ModifyMonth=month, State="Delete").sum('MemoryLimit'))
    for _i in xrange(0, len(seven_month_list)):
        data['data3'].append(data['data1'][_i] + data['data2'][_i])
    return JsonResponse(data, safe=False)
