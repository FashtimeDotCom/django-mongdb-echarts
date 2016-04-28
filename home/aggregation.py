# coding:utf8
from .models import Db


# 获得某月存量
def get_duration_by_month(month=None):
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
    cur = Db._get_collection().aggregate(pipeline)
    result = cur.next()
    cur.close()
    return result['count']


# 获得某周存量
def get_duration_by_week(week=None):
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
    cur = Db._get_collection().aggregate(pipeline)
    result = cur.next()
    cur.close()
    return result['count']


# 获得某日存量
def get_duration_by_day(day=None):
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
    cur = Db._get_collection().aggregate(pipeline)
    # 聚合结果存下来
    result = cur.next()
    # 关闭游标
    cur.close()
    # 返回结果
    return result['count']


# 获得月净增
def get_delta_by_month(month=None):

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
def get_delta_by_week(week=None):

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
def get_delta_by_day(day=None):

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


# 获得limit个公司磁盘总量结果的游标
def get_top_disk_space_sum_of_company(limit=None):
    pipeline = [
        {
            '$match': {
                'InnerMark': 'No',
                'State': {'$ne': 'Delete'}
            }
        },
        {
            '$group': {
                '_id': "$CompanyName",
                'SumDiskSpace': {'$sum': "$DiskSpace"},
            }
        },
        {
            '$sort': {'SumDiskSpace': -1}
        },
        {'$limit': limit}
    ]
    cur = Db._get_collection().aggregate(pipeline)
    tmp_list = []
    result = []
    for _ in xrange(0, limit):
        tmp_list.append(cur.next())
    cur.close()
    for i in xrange(0, limit):
        result.append({'value': tmp_list[i]['SumDiskSpace'] / 1024, 'name': tmp_list[i]['_id']})
    return result


# 获得limit个公司内存总量结果的游标
def get_top_memory_limit_sum_of_company(limit=None):
    pipeline = [
        {
            '$match': {
                'InnerMark': 'No',
                'State': {'$ne': 'Delete'}
            }
        },
        {
            '$group': {
                '_id': "$CompanyName",
                'SumMemoryLimit': {'$sum': "$MemoryLimit"},
            }
        },
        {
            '$sort': {'SumMemoryLimit': -1}
        },
        {'$limit': limit}
    ]
    cur = Db._get_collection().aggregate(pipeline)
    tmp_list = []
    result = []
    for _ in xrange(0, limit):
        tmp_list.append(cur.next())
    cur.close()
    for i in xrange(0, limit):
        result.append({'value': tmp_list[i]['SumMemoryLimit'] / 1024, 'name': tmp_list[i]['_id']})
    return result


# 获得limit个行业磁盘总量结果的游标
def get_top_disk_space_sum_of_industry(limit=None):
    pipeline = [
        {
            '$match': {
                'InnerMark': 'No',
                'State': {'$ne': 'Delete'}
            }
        },
        {
            '$group': {
                '_id': "$Industry",
                'SumDiskSpace': {'$sum': "$DiskSpace"},
            }
        },
        {
            '$sort': {'SumDiskSpace': -1}
        },
        {'$limit': limit}
    ]
    cur = Db._get_collection().aggregate(pipeline)
    tmp_list = []
    result = []
    for _ in xrange(0, limit):
        tmp_list.append(cur.next())
    cur.close()
    for i in xrange(0, limit):
        result.append({'value': tmp_list[i]['SumDiskSpace'] / 1024, 'name': tmp_list[i]['_id']})
    return result


# 获得limit个行业内存总量结果的游标
def get_top_memory_limit_sum_of_industry(limit=None):
    pipeline = [
        {
            '$match': {
                'InnerMark': 'No',
                'State': {'$ne': 'Delete'}
            }
        },
        {
            '$group': {
                '_id': "$Industry",
                'SumMemoryLimit': {'$sum': "$MemoryLimit"},
            }
        },
        {
            '$sort': {'SumMemoryLimit': -1}
        },
        {'$limit': limit}
    ]
    cur = Db._get_collection().aggregate(pipeline)
    tmp_list = []
    result = []
    for _ in xrange(0, limit):
        tmp_list.append(cur.next())
    cur.close()
    for i in xrange(0, limit):
        result.append({'value': tmp_list[i]['SumMemoryLimit'] / 1024, 'name': tmp_list[i]['_id']})
    return result


# 获得某周top limit 个公司实例个数净新增的游标
def get_top_pure_increase_of_company(week=None, limit=None):
    pipeline = [
        {
            '$match': {
                'InnerMark': 'No',
                'BusinessCreateWeek': {'$eq': week},
                'BusinessDeleteWeek': {'$ne': None},
            },
        },
        {
            '$group': {
                '_id': "$CompanyName",
                'manager': {'$first': "$Manager"},
                'count': {'$sum': 1},
            }
        },
        {
            '$sort': {'count': -1}
        },
        {'$limit': limit}
    ]
    cur = Db._get_collection().aggregate(pipeline)
    tmp_list = []
    result = []
    for _ in xrange(0, limit):
        tmp_list.append(cur.next())
    cur.close()
    for i in xrange(0, limit):
        result.append({'value': tmp_list[i]['count'], 'name': tmp_list[i]['_id'] + '(' + tmp_list[i]['manager'] + ')'})
    return result

# 笔记区---------------
a = [
    {'$match':{"deleted":0}},
    {'$project':{'user_email':1,'company_id':1,'top_organization_id':1,'deleted':1,'region':1}},
    {'$group': {'_id': "$user_email", 'uhost_count':{'$sum':1},'regions':{'$addToSet':"$region"}}},
    {'$match':{'regions':{'$all':["7001"]}},},
    {'$sort':{'uhost_count':-1}},
    {'$match':{'regions':{'$size':1}},}
]