# coding:utf8
from __future__ import division
# Create your views here.
from django.views.generic import TemplateView
import calendar
from datetime import timedelta
import time
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, HttpResponse
import pytz
import datetime
from operator import itemgetter
from aggregation import *
from aggregation_company import *
from aggregation_ha import *
from aggregation_self_build import *
import math
from home.models import Db_HA
from .permission import check_permission

global zero_time, zero_timestamp
zero_timestamp = 1357488000
# = 2013-01-07 00:00
zero_time = time.localtime(zero_timestamp)
# time.struct_time(tm_year=2013, tm_mon=1, tm_mday=1, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=1, tm_yday=1, tm_isdst=0)


class EchartsIndexView(TemplateView):
    template_name = "home/echarts.html"
    permission = "sessions.add_session"

    def dispatch(self, *args, **kwargs):
        username = self.request.META.get("user")
        if username:
            if not check_permission(username, self.permission):
                return HttpResponse(
                    "权限({0})：空<br>联系人：ernest.luo@ucloud.cn<br>操作人：kevin.gao@ucloud.cn<br>首次登陆".format(
                        username)
                )
            return super(EchartsIndexView, self).dispatch(*args, **kwargs)
        else:
            if not self.request.user.has_perm(self.permission):
                return HttpResponse(
                    "权限({0})：空<br>联系人：ernest.luo@ucloud.cn<br>操作人：kevin.gao@ucloud.cn<br>非首次登陆".format(
                        self.request.user)
                )
            return super(EchartsIndexView, self).dispatch(*args, **kwargs)


def business_week_to_date(week=None):
    timestamp = (week - 1) * 86400 * 7 + zero_timestamp
    local_dt = datetime.datetime.fromtimestamp(timestamp)
    return local_dt.strftime('%m-%d')


# 数据库转换为local时间，不需要了
def utc_to_local(utc_dt):
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)


# 数据库转换为local时间，不需要了
def local_to_utc(local_dt, time_zone):
    local = pytz.timezone(time_zone)
    local_dt = local.localize(local_dt, is_dst=None)
    return local_dt.astimezone(pytz.utc)


# print "共{}个".format(Db.objects.count())


def field_count(field):
    data = dict()
    data['field_list'] = list(Db.objects.all().distinct(field))
    exec("data['count_list'] = "
         "[Db.objects({}=c).count() for c in data['field_list']]").format(field)
    return data


@csrf_exempt
def outer_dbclass(request):
    data = {
        'data': Db.outer.order_by('DBClass').distinct('DBType'),
        'data1': [],
        'data2': [],
        'data3': [],
    }
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
        else:
            for v in Db.outer(DBClass=dbclass).distinct('DBType'):
                data['data3'].append({'value': Db.outer(DBClass=dbclass, DBType=v).count(), 'name': v})
    return JsonResponse(data, safe=False)


@csrf_exempt
def outer_disk_type(request):
    data = {
        'data': Db.outer.order_by('DBClass').distinct('DiskType'),
        'data1': []
    }
    for disktype in data['data']:
        data['data1'].append({'value': Db.outer(DiskType=disktype).count(), 'name': disktype})
    return JsonResponse(data, safe=False)


@csrf_exempt
def outer_group_region(request):
    data = {
        'data': Db.outer.order_by('DBClass').distinct('AzGroup'),
        'data1': [],
        'data2': [],
    }
    for azgroup in data['data']:
        data['data1'].append({'value': Db.outer(AzGroup=azgroup).count(), 'name': azgroup})
        for region in Db.outer(AzGroup=azgroup).order_by('DBClass').distinct('Region'):
            data['data2'].append({'value': Db.outer(AzGroup=azgroup, Region=region).count(), 'name': region})
    return JsonResponse(data, safe=False)


# 需求改变，so...废弃
@csrf_exempt
def outer_disk_type_backup(request):
    data = {
        'data': Db.outer.order_by('DBClass').distinct('DiskType'),
        'data1': [],
        'data2': [],
        'data3': [],
    }
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
            for v in Db.outer(DBClass=dbclass, ClusterId='').distinct('DiskType'):
                data['data3'].append({'value': Db.outer(DBClass=dbclass, ClusterId='', DiskType=v).count(), 'name': v})
            # HA
            for v in Db.outer(DBClass=dbclass, ClusterId__ne='').distinct('DiskType'):
                data['data3'].append({'value': Db.outer(DBClass=dbclass, ClusterId__ne='', DiskType=v).count(), 'name': v})
        else:
            for v in Db.outer(DBClass=dbclass).distinct('DiskType'):
                data['data3'].append({'value': Db.outer(DBClass=dbclass, DiskType=v).count(), 'name': v})
    return JsonResponse(data, safe=False)
# 需求改变，so...废弃


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
def top_10_industry_count(request):
    data = {
        'data': [],
        'data1': []
    }
    top_10_industry_tuple = []
    industries = Db.outer.item_frequencies('Industry', normalize=True)
    top_industries = sorted(industries.items(), key=itemgetter(1), reverse=True)[:10]
    for t, _ in top_industries:
        top_10_industry_tuple.append((t, Db.outer(Industry=t).count()))
    # 图左下角的列表
    data['data'] = [i for i, _ in top_10_industry_tuple]
    for industry, count in top_10_industry_tuple:
        data['data1'].append({'value': count, 'name': industry})
    return JsonResponse(data, safe=False)


@csrf_exempt
def top_10_industry_count_further(request):
    industry = request.GET['Industry']
    db_version_list = Db.outer(Industry=industry).distinct('DBType')
    db_class_list = Db.outer(Industry=industry).distinct('DBClass')
    data = dict()
    # 图左下角的列表
    data = {
        'title': u"*{}*".format(industry),
        'data': db_version_list,
        'data1': [],
        'data2': [],
        'data3': [],
        'data4': [],
        'data5': [],
    }
    # 环装饼图 ------------
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
    # 饼图 disk type
    data['data4'] = Db.outer(Industry=industry).order_by('DBClass').distinct('DiskType')
    for disktype in data['data4']:
        data['data5'].append({'value': Db.outer(Industry=industry, DiskType=disktype).count(), 'name': disktype})
    return JsonResponse(data, safe=False)


@csrf_exempt
def top_10_industry_memory_limit(request):
    data = {
        'category': [],
        'data1': get_top_memory_limit_sum_of_industry(10)
    }
    data['category'] = [i for _, i in [j.items()[0] for j in data['data1']]]
    return JsonResponse(data, safe=False)


@csrf_exempt
def top_10_industry_disk_space(request):
    data = {
        'category': [],
        'data1': get_top_disk_space_sum_of_industry(10)
    }
    data['category'] = [i for _, i in [j.items()[0] for j in data['data1']]]
    return JsonResponse(data, safe=False)


@csrf_exempt
def top_10_company_count(request):
    data = {
        'category': [],
        'data1': [],
    }
    top_10_company_list = []
    companies = Db.outer.item_frequencies('CompanyName', normalize=True)
    top_companies = sorted(companies.items(), key=itemgetter(1), reverse=True)[:10]
    for t, _ in top_companies:
        top_10_company_list.append((t, Db.outer(CompanyName=t).count()))
    # 图左下角的列表
    data['category'] = [i for i, _ in top_10_company_list]
    for company, count in top_10_company_list:
        data['data1'].append({'value': count, 'name': company})
    return JsonResponse(data, safe=False)


@csrf_exempt
def top_10_company_count_further(request):
    company = request.GET['CompanyName']
    db_version_list = Db.outer(CompanyName=company).distinct('DBType')
    db_class_list = Db.outer(CompanyName=company).distinct('DBClass')
    data = {

        'title': u"*{}*".format(company),
        'category': db_version_list,
        'data1': [],
        'data2': [],
        'data3': [],
        'data4': [],
        'data5': [],
    }
    # 环装饼图 ------------
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
    # 饼图 disk type
    data['data4'] = Db.outer(CompanyName=company).order_by('DBClass').distinct('DiskType')
    for disktype in data['data4']:
        data['data5'].append({'value': Db.outer(CompanyName=company, DiskType=disktype).count(), 'name': disktype})
    return JsonResponse(data, safe=False)


@csrf_exempt
def top_10_company_memory_limit(request):
    data = {
        'category': [],
        'data1': get_top_memory_limit_sum_of_company(10)
    }
    data['category'] = [i for _, i in [j.items()[0] for j in data['data1']]]
    return JsonResponse(data, safe=False)


@csrf_exempt
def top_10_company_disk_space(request):
    data = {
        'category': [],
        'data1': get_top_disk_space_sum_of_company(10)
    }
    data['category'] = [i for _, i in [j.items()[0] for j in data['data1']]]
    return JsonResponse(data, safe=False)


@csrf_exempt
def top_10_company_pure_increase_week(request):
    _local_now = datetime.datetime.now()
    current_timestamp = time.mktime(_local_now.timetuple())
    current_business_week = int(math.ceil((current_timestamp - zero_timestamp) / 604800))
    print '本周:{0}'.format(current_business_week)
    tmpbook = get_top_pure_increase_of_company(week=current_business_week - 1, limit=10)
    data = {
        'category': [i for _, i in [j.items()[0] for j in tmpbook]],
        'data1': tmpbook
    }
    return JsonResponse(data, safe=False)


@csrf_exempt
def top_10_company_pure_delete_week(request):
    _local_now = datetime.datetime.now()
    current_timestamp = time.mktime(_local_now.timetuple())
    current_business_week = int(math.ceil((current_timestamp - zero_timestamp) / 604800))
    tmpbook = get_top_pure_delete_of_company(week=current_business_week - 1, limit=10)
    data = {
        'category': [i for _, i in [j.items()[0] for j in tmpbook]],
        'data1': tmpbook
    }
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


@csrf_exempt
def fish_bone_disk_by_month(request):
    data = {
        'title': 'Disk净新增(TB)',
        'data1': [],
        'data2': [],
        'data3': [],
    }
    _local_now = datetime.datetime.now()
    current_business_month = (_local_now.year - zero_time.tm_year) * 12 + _local_now.month
    twelve_business_month = xrange(current_business_month-5, current_business_month+1)
    data['y'] = [u'{}月'.format(12 if month % 12 == 0 else month % 12) for month in twelve_business_month]
    # seven_month_list = [month for month in range(_local_now.month - 11, _local_now.month+1) if month > 0]
    # data['y'] = ["{}月".format(_i) for _i in seven_month_list]
    for month in twelve_business_month:
        data['data1'].append(int(round(Db.outer_all(BusinessCreateMonth=month).sum('DiskSpace') / 1024)))
        data['data2'].append(int(round(0 - Db.outer_all_deleted(BusinessDeleteMonth=month,).sum('DiskSpace') / 1024)))
    for _i in xrange(0, len(twelve_business_month)):
        data['data3'].append(data['data1'][_i] + data['data2'][_i])
    return JsonResponse(data, safe=False)


@csrf_exempt
def fish_bone_memory_by_month(request):
    data = {
        'title': 'Memory净新增(GB)',
        'data1': [],
        'data2': [],
        'data3': [],
    }
    _local_now = datetime.datetime.now()
    current_business_month = (_local_now.year - zero_time.tm_year) * 12 + _local_now.month
    twelve_business_month = xrange(current_business_month-5, current_business_month+1)
    data['y'] = [u'{}月'.format(12 if month % 12 == 0 else month % 12) for month in twelve_business_month]
    for month in twelve_business_month:
        # 当月创建
        data['data1'].append(int(round(Db.outer_all(BusinessCreateMonth=month).sum('MemoryLimit') / 1024)))
        # 当月删除
        data['data2'].append(int(round(0 - Db.outer_all_deleted(BusinessDeleteMonth=month,).sum('MemoryLimit') / 1024)))
    for _i in xrange(0, len(twelve_business_month)):
        data['data3'].append(data['data1'][_i] + data['data2'][_i])
    return JsonResponse(data, safe=False)


@csrf_exempt
def instance_pure_increase(request):
    time_grading = request.GET['time_grading']
    data = {
        'title': "",
        # 分别是data1、2、3、4
        'legend': ['申请', '删除', '净增', '存量'],
        'xAxis': [],
        'data1': [],
        'data2': [],
        'data3': [],
        'data4': [],
    }
    # 月粒度
    if time_grading == 'month':
        data['title'] = "所有实例 数量申请/删除/净增/存量（月）"
        _local_now = datetime.datetime.now()
        current_business_month = (_local_now.year - zero_time.tm_year) * 12 + _local_now.month
        twelve_business_month = xrange(current_business_month-11, current_business_month+1)
        data['xAxis'] = [u'{}月'.format(12 if month % 12 == 0 else month % 12) for month in twelve_business_month]
        # 当月申请
        for month in twelve_business_month:
            data['data1'].append(Db.outer_all(BusinessCreateMonth=month).count())
        # 当月删除
        for month in twelve_business_month:
            data['data2'].append(Db.outer_all_deleted(BusinessDeleteMonth=month).count())
        # 净申请
        for _i in xrange(0, len(twelve_business_month)):
            data['data3'].append(data['data1'][_i] - data['data2'][_i])

        # 存量
        for month in twelve_business_month:
            data['data4'].append(get_duration_by_month(month))
    # 周粒度
    elif time_grading == 'week':
        data['title'] = "所有实例 数量申请/删除/净增/存量（周）"
        _local_now = datetime.datetime.now()
        current_timestamp = time.mktime(_local_now.timetuple())
        current_business_week = int(math.ceil((current_timestamp - zero_timestamp) / 604800))
        fifteen_business_week = xrange(current_business_week-14, current_business_week+1)
        data['xAxis'] = [u'{}'.format(business_week_to_date(week)) for week in fifteen_business_week]
        # 当周申请
        for week in fifteen_business_week:
            data['data1'].append(Db.outer_all(BusinessCreateWeek=week).count())
        # 当周删除
        for week in fifteen_business_week:
            data['data2'].append(Db.outer_all_deleted(BusinessDeleteWeek=week).count())
        # 净申请
        for _i in xrange(0, len(fifteen_business_week)):
            data['data3'].append(data['data1'][_i] - data['data2'][_i])
        # 存量
        for week in fifteen_business_week:
            data['data4'].append(get_duration_by_week(week))
    # 天粒度
    elif time_grading == 'day':
        data['title'] = "所有实例 数量申请/删除/净增/存量（日）"
        _local_now = datetime.datetime.now()
        current_timestamp = time.mktime(_local_now.timetuple())
        current_business_day = int(math.ceil((current_timestamp - zero_timestamp) / 86400))
        thirty_business_day = xrange(current_business_day - 29, current_business_day + 1)
        data['xAxis'] = [u'{}'.format((_local_now + timedelta(days=i)).strftime('%d')) for i in range(-29, 1)]
        # 当日申请
        for day in thirty_business_day:
            data['data1'].append(Db.outer_all(BusinessCreateDay=day).count())
        # 当日删除
        for day in thirty_business_day:
            data['data2'].append(Db.outer_all_deleted(BusinessDeleteDay=day).count())
        # 净申请
        for _i in xrange(0, len(thirty_business_day)):
            data['data3'].append(data['data1'][_i] - data['data2'][_i])
        # 存量
        for day in thirty_business_day:
            data['data4'].append(get_duration_by_day(day))
    else:
        pass
    # print data
    return JsonResponse(data, safe=False)

# 二期需求开始


@csrf_exempt
def instance_pure_increase_by_company(request):
    time_grading = request.GET['time_grading']
    company_name = request.GET['company_name']
    data = {
        'title': "",
        # 分别是data1、2、3、4
        'legend': ['申请', '删除', '净增', '存量'],
        'xAxis': [],
        'data1': [],
        'data2': [],
        'data3': [],
        'data4': [],
    }
    # 月粒度
    if time_grading == 'month':
        # data['title'] = "实例数量申请/删除/净增/存量"
        data['title'] = company_name
        _local_now = datetime.datetime.now()
        current_business_month = (_local_now.year - zero_time.tm_year) * 12 + _local_now.month
        twelve_business_month = xrange(current_business_month-11, current_business_month+1)
        data['xAxis'] = [u'{}月'.format(12 if month % 12 == 0 else month % 12) for month in twelve_business_month]
        # 当月申请
        for month in twelve_business_month:
            data['data1'].append(Db.outer_all(BusinessCreateMonth=month, CompanyName=company_name).count())
        # 当月删除
        for month in twelve_business_month:
            data['data2'].append(Db.outer_all_deleted(BusinessDeleteMonth=month, CompanyName=company_name).count())
        # 净申请
        for _i in xrange(0, len(twelve_business_month)):
            data['data3'].append(data['data1'][_i] - data['data2'][_i])

        # 存量
        for month in twelve_business_month:
            data['data4'].append(get_duration_by_month_and_company(month, company_name))
    # 周粒度
    elif time_grading == 'week':
        # data['title'] = "最近15周实例净增"
        data['title'] = company_name
        _local_now = datetime.datetime.now()
        current_timestamp = time.mktime(_local_now.timetuple())
        current_business_week = int(math.ceil((current_timestamp - zero_timestamp) / 604800))
        fifteen_business_week = xrange(current_business_week-14, current_business_week+1)
        data['xAxis'] = [u'{}'.format(business_week_to_date(week)) for week in fifteen_business_week]
        # 当周申请
        for week in fifteen_business_week:
            data['data1'].append(Db.outer_all(BusinessCreateWeek=week, CompanyName=company_name).count())
        # 当周删除
        for week in fifteen_business_week:
            data['data2'].append(Db.outer_all_deleted(BusinessDeleteWeek=week, CompanyName=company_name).count())
        # 净申请
        for _i in xrange(0, len(fifteen_business_week)):
            data['data3'].append(data['data1'][_i] - data['data2'][_i])
        # 存量
        for week in fifteen_business_week:
            data['data4'].append(get_duration_by_week_and_company(week, company_name))
    # 天粒度
    elif time_grading == 'day':
        # data['title'] = "最近30天实例净增"
        data['title'] = company_name
        _local_now = datetime.datetime.now()
        current_timestamp = time.mktime(_local_now.timetuple())
        current_business_day = int(math.ceil((current_timestamp - zero_timestamp) / 86400))
        thirty_business_day = xrange(current_business_day - 29, current_business_day + 1)
        data['xAxis'] = [u'{}'.format((_local_now + timedelta(days=i)).strftime('%d')) for i in range(-29, 1)]
        # 当日申请
        for day in thirty_business_day:
            data['data1'].append(Db.outer_all(BusinessCreateDay=day, CompanyName=company_name).count())
        # 当日删除
        for day in thirty_business_day:
            data['data2'].append(Db.outer_all_deleted(BusinessDeleteDay=day, CompanyName=company_name).count())
        # 净申请
        for _i in xrange(0, len(thirty_business_day)):
            data['data3'].append(data['data1'][_i] - data['data2'][_i])
        # 存量
        for day in thirty_business_day:
            data['data4'].append(get_duration_by_day_and_company(day, company_name))
    else:
        pass
    # print data
    return JsonResponse(data, safe=False)


@csrf_exempt
def fish_bone_disk_by_month_company(request):
    company_name = request.GET['CompanyName']
    data = {
        'title': 'Disk净新增(TB)',
        'data1': [],
        'data2': [],
        'data3': [],
    }
    _local_now = datetime.datetime.now()
    current_business_month = (_local_now.year - zero_time.tm_year) * 12 + _local_now.month
    twelve_business_month = xrange(current_business_month-5, current_business_month+1)
    data['y'] = [u'{}月'.format(12 if month % 12 == 0 else month % 12) for month in twelve_business_month]
    # seven_month_list = [month for month in range(_local_now.month - 11, _local_now.month+1) if month > 0]
    # data['y'] = ["{}月".format(_i) for _i in seven_month_list]
    for month in twelve_business_month:
        data['data1'].append(int(round(Db.outer_all(BusinessCreateMonth=month, CompanyName=company_name).sum('DiskSpace') / 1024)))
        data['data2'].append(int(round(0 - Db.outer_all_deleted(BusinessDeleteMonth=month, CompanyName=company_name).sum('DiskSpace') / 1024)))
    for _i in xrange(0, len(twelve_business_month)):
        data['data3'].append(data['data1'][_i] + data['data2'][_i])
    return JsonResponse(data, safe=False)


@csrf_exempt
def fish_bone_memory_by_month_company(request):
    company_name = request.GET['CompanyName']
    data = {
        'title': 'Memory净新增(GB)',
        'data1': [],
        'data2': [],
        'data3': [],
    }
    _local_now = datetime.datetime.now()
    current_business_month = (_local_now.year - zero_time.tm_year) * 12 + _local_now.month
    twelve_business_month = xrange(current_business_month-5, current_business_month+1)
    data['y'] = [u'{}月'.format(12 if month % 12 == 0 else month % 12) for month in twelve_business_month]
    for month in twelve_business_month:
        # 当月创建
        data['data1'].append(int(round(Db.outer_all(BusinessCreateMonth=month, CompanyName=company_name).sum('MemoryLimit') / 1024)))
        # 当月删除
        data['data2'].append(int(round(0 - Db.outer_all_deleted(BusinessDeleteMonth=month, CompanyName=company_name).sum('MemoryLimit') / 1024)))
    for _i in xrange(0, len(twelve_business_month)):
        data['data3'].append(data['data1'][_i] + data['data2'][_i])
    return JsonResponse(data, safe=False)


@csrf_exempt
def instance_pure_increase_ha(request):
    time_grading = request.GET['time_grading']
    data = {
        'title': "",
        # 分别是data1、2、3、4
        'legend': ['申请', '删除', '净增', '存量'],
        'xAxis': [],
        'data1': [],
        'data2': [],
        'data3': [],
        'data4': [],
    }
    # 月粒度
    if time_grading == 'month':
        data['title'] = "高可用实例 数量申请/删除/净增/存量（月）"
        _local_now = datetime.datetime.now()
        current_business_month = (_local_now.year - zero_time.tm_year) * 12 + _local_now.month
        twelve_business_month = xrange(current_business_month-11, current_business_month+1)
        data['xAxis'] = [u'{}月'.format(12 if month % 12 == 0 else month % 12) for month in twelve_business_month]
        # 当月申请
        for month in twelve_business_month:
            # , InstanceMode='HA'
            data['data1'].append(Db_HA.outer_all(BusinessCreateMonth=month).count())
        # 当月删除
        for month in twelve_business_month:
            data['data2'].append(Db_HA.outer_all_deleted(BusinessDeleteMonth=month).count())
        # 净申请
        for _i in xrange(0, len(twelve_business_month)):
            data['data3'].append(data['data1'][_i] - data['data2'][_i])

        # 存量
        print twelve_business_month
        for month in twelve_business_month:
            data['data4'].append(get_duration_by_month_and_ha(month))
    # 周粒度
    elif time_grading == 'week':
        data['title'] = "高可用实例 数量申请/删除/净增/存量（周）"
        _local_now = datetime.datetime.now()
        current_timestamp = time.mktime(_local_now.timetuple())
        current_business_week = int(math.ceil((current_timestamp - zero_timestamp) / 604800))
        fifteen_business_week = xrange(current_business_week-14, current_business_week+1)
        data['xAxis'] = [u'{}'.format(business_week_to_date(week)) for week in fifteen_business_week]
        # 当周申请
        for week in fifteen_business_week:
            data['data1'].append(Db_HA.outer_all(BusinessCreateWeek=week).count())
        # 当周删除
        for week in fifteen_business_week:
            data['data2'].append(Db_HA.outer_all_deleted(BusinessDeleteWeek=week).count())
        # 净申请
        for _i in xrange(0, len(fifteen_business_week)):
            data['data3'].append(data['data1'][_i] - data['data2'][_i])
        # 存量
        for week in fifteen_business_week:
            data['data4'].append(get_duration_by_week_and_ha(week))
    # 天粒度
    elif time_grading == 'day':
        data['title'] = "高可用实例 数量申请/删除/净增/存量（日）"
        _local_now = datetime.datetime.now()
        current_timestamp = time.mktime(_local_now.timetuple())
        current_business_day = int(math.ceil((current_timestamp - zero_timestamp) / 86400))
        thirty_business_day = xrange(current_business_day - 29, current_business_day + 1)
        data['xAxis'] = [u'{}'.format((_local_now + timedelta(days=i)).strftime('%d')) for i in range(-29, 1)]
        # 当日申请
        for day in thirty_business_day:
            data['data1'].append(Db_HA.outer_all(BusinessCreateDay=day).count())
        # 当日删除
        for day in thirty_business_day:
            data['data2'].append(Db_HA.outer_all_deleted(BusinessDeleteDay=day).count())
        # 净申请
        for _i in xrange(0, len(thirty_business_day)):
            data['data3'].append(data['data1'][_i] - data['data2'][_i])
        # 存量
        for day in thirty_business_day:
            data['data4'].append(get_duration_by_day_and_ha(day))
    else:
        pass
    return JsonResponse(data, safe=False)


@csrf_exempt
def top_10_self_build_instance_count(request):
    _ = get_top_10_self_build_instance_count(limit=100)
    data = {
        'data': _
    }
    return JsonResponse(data, safe=False)

