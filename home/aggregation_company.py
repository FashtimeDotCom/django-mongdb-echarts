# coding:utf8
from .models import Db


# 获得某月存量
def get_duration_by_month_and_company(month=None, company_name=None):
    pipeline = [
        {
            '$match': {'InnerMark': 'No',
                       'CompanyName': company_name}
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
    cur = Db._get_collection().aggregate(pipeline)
    result = cur.next()
    cur.close()
    return result['count']


# 获得某周存量
def get_duration_by_week_and_company(week=None, company_name=None):
    pipeline = [
        {
            '$match': {'InnerMark': 'No',
                       'CompanyName': company_name}
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
    cur = Db._get_collection().aggregate(pipeline)
    result = cur.next()
    cur.close()
    return result['count']


# 获得某日存量
def get_duration_by_day_and_company(day=None, company_name=None):
    pipeline = [
        {
            '$match': {'InnerMark': 'No',
                       'CompanyName': company_name}
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
    cur = Db._get_collection().aggregate(pipeline)
    # 聚合结果存下来
    result = cur.next()
    # 关闭游标
    cur.close()
    # 返回结果
    return result['count']


# --------
# 获得月净增
def get_delta_by_month_and_company(month=None):

    pipeline_create = [
        {
            '$match': {'InnerMark': 'No'}
        },
        {
            '$project': {
                # "D": "$DiskSpace",
                # "M": "$MemoryLimit",
                'cmp': {
                    '$eq': ["$BusinessCreateMonth", month]
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

    pipeline_delete = [
        {
            '$match': {'InnerMark': 'No'}
        },
        {
            '$project': {
                # "D": "$DiskSpace",
                # "M": "$MemoryLimit",
                'cmp': {
                    '$eq': ["$BusinessDeleteMonth", month]
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
    cur_create = Db._get_collection().aggregate(pipeline_create)
    cur_delete = Db._get_collection().aggregate(pipeline_delete)
    # 聚合结果存下来
    create = cur_create.next()
    delete = cur_delete.next()
    # 关闭游标
    cur_create.close()
    cur_delete.close()
    # 返回结果
    return create['count'] - delete['count']


# 获得周净增
def get_delta_by_week_and_company(week=None, company=None):

    pipeline_create = [
        {
            '$match': {'InnerMark': 'No'}
        },
        {
            '$project': {
                # "D": "$DiskSpace",
                # "M": "$MemoryLimit",
                'cmp': {
                    '$eq': ["$BusinessCreateWeek", week]
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

    pipeline_delete = [
        {
            '$match': {'InnerMark': 'No'}
        },
        {
            '$project': {
                # "D": "$DiskSpace",
                # "M": "$MemoryLimit",
                'cmp': {
                    '$eq': ["$BusinessDeleteWeek", week]
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
    cur_create = Db._get_collection().aggregate(pipeline_create)
    cur_delete = Db._get_collection().aggregate(pipeline_delete)
    # 聚合结果存下来
    create = cur_create.next()
    delete = cur_delete.next()
    # 关闭游标
    cur_create.close()
    cur_delete.close()
    # 返回结果
    return create['count'] - delete['count']


# 获得日净增
def get_delta_by_day_and_company(day=None, company=None):

    pipeline_create = [
        {
            '$match': {'InnerMark': 'No'}
        },
        {
            '$project': {
                # "D": "$DiskSpace",
                # "M": "$MemoryLimit",
                'cmp': {
                    '$eq': ["$BusinessCreateDay", day]
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

    pipeline_delete = [
        {
            '$match': {'InnerMark': 'No'}
        },
        {
            '$project': {
                # "D": "$DiskSpace",
                # "M": "$MemoryLimit",
                'cmp': {
                    '$eq': ["$BusinessDeleteDay", day]
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
    cur_create = Db._get_collection().aggregate(pipeline_create)
    cur_delete = Db._get_collection().aggregate(pipeline_delete)
    # 聚合结果存下来
    create = cur_create.next()
    delete = cur_delete.next()
    # 关闭游标
    cur_create.close()
    cur_delete.close()
    # 返回结果
    return create['count'] - delete['count']