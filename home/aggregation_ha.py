# coding:utf8
from .models import Db_HA


# 获得某月存量
def get_duration_by_month_and_ha(month=None):
    pipeline = [
        {
            '$match': {'InnerMark': 'No'}
        },
        {
            '$project': {
                # "D": "$DiskSpace",
                # "M": "$MemoryLimit",
                # "duration": {'$subtract': ['$DiskSpace', '$MemoryLimit']},
                'cmp': {
                    '$and': [
                        {
                            '$lte': ["$BusinessCreateMonth", month]
                        },
                        {
                            '$or': [
                                {'$gt': ["$BusinessDeleteMonth", month]},
                                {'$eq': ['$DeleteTime', None]}
                            ]
                        }
                    ]
                }
            }
        },
        {
            '$match': {'cmp': True}
        },
        {
            '$group': {
                '_id': "$cmp",
                'count': {'$sum': 1},
                # 'disk_count': {'$sum': '$D'},
                # 'memory_count': {'$sum': '$M'},
            }
        }
    ]
    cur = Db_HA._get_collection().aggregate(pipeline)
    try:
        result = cur.next()
    except StopIteration:
        return 0
    cur.close()
    return result['count']


# 获得某周存量
def get_duration_by_week_and_ha(week=None):
    pipeline = [
        {
            '$match': {'InnerMark': 'No'}
        },
        {
            '$project': {
                # "D": "$DiskSpace",
                # "M": "$MemoryLimit",
                'cmp': {
                    '$and': [
                        {
                            '$lte': ["$BusinessCreateWeek", week]
                        },
                        {
                            '$or': [
                                {'$gt': ["$BusinessDeleteWeek", week]},
                                {'$eq': ['$DeleteTime', None]}
                            ]
                        }
                    ]
                }
            }
        },
        {
            '$match': {'cmp': True}
        },
        {
            '$group': {
                '_id': "$cmp",
                'count': {'$sum': 1},
                # 'disk_count': {'$sum': '$D'},
                # 'memory_count': {'$sum': '$M'}
            }
        }
    ]
    cur = Db_HA._get_collection().aggregate(pipeline)
    try:
        result = cur.next()
    except StopIteration:
        return 0
    cur.close()
    return result['count']


# 获得某日存量
def get_duration_by_day_and_ha(day=None):
    pipeline = [
        {
            '$match': {'InnerMark': 'No'}
        },
        {
            '$project': {
                # "D": "$DiskSpace",
                # "M": "$MemoryLimit",
                'cmp': {
                    '$and': [
                        {
                            '$lte': ["$BusinessCreateDay", day]
                        },
                        {
                            '$or': [
                                {'$gt': ["$BusinessDeleteDay", day]},
                                {'$eq': ['$DeleteTime', None]}
                            ]
                        }
                    ]
                }
            }
        },
        {
            '$match': {'cmp': True}
        },
        {
            '$group': {
                '_id': "$cmp",
                'count': {'$sum': 1},
                # 'disk_count': {'$sum': '$D'},
                # 'memory_count': {'$sum': '$M'}
            }
        }
    ]
    # 创建游标
    cur = Db_HA._get_collection().aggregate(pipeline)
    # 聚合结果存下来
    try:
        result = cur.next()
    except StopIteration:
        return 0
    # 关闭游标
    cur.close()
    # 返回结果
    return result['count']
