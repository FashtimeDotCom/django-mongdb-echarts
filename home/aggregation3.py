# coding:utf8
from .models import Db


# 获得内存某月存量
def get_memory_diskspace_total_by_month(month=None,):
    pipeline = [
        {
            '$match': {'InnerMark': 'No'}
        },
        {
            '$project': {
                "D": "$DiskSpace",
                "M": "$MemoryLimit",
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
                # 'count': {'$sum': 1},
                'disk_count': {'$sum': '$D'},
                'memory_count': {'$sum': '$M'},
            }
        }
    ]
    cur = Db._get_collection().aggregate(pipeline)
    result = cur.next()
    cur.close()
    return result


# 获得内存某周存量
def get_memory_diskspace_total_by_week(week=None,):
    pipeline = [
        {
            '$match': {'InnerMark': 'No'}
        },
        {
            '$project': {
                "D": "$DiskSpace",
                "M": "$MemoryLimit",
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
                # 'count': {'$sum': 1},
                'disk_count': {'$sum': '$D'},
                'memory_count': {'$sum': '$M'},
            }
        }
    ]
    cur = Db._get_collection().aggregate(pipeline)
    result = cur.next()
    cur.close()
    return result


# 获得内存某日存量
def get_memory_diskspace_total_by_day(day=None,):
    pipeline = [
        {
            '$match': {'InnerMark': 'No'}
        },
        {
            '$project': {
                "D": "$DiskSpace",
                "M": "$MemoryLimit",
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
                # 'count': {'$sum': 1},
                'disk_count': {'$sum': '$D'},
                'memory_count': {'$sum': '$M'},
            }
        }
    ]
    cur = Db._get_collection().aggregate(pipeline)
    result = cur.next()
    cur.close()
    return result
