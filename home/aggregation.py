# coding:utf8
from .models import Db


# 获得某月存续
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


# 获得某周存续
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


# 获得某日存续
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

# 笔记区---------------
pipeline = [
    {
        '$match': {

        }
    },
    {},
    {}
]

a = {
    "_id" : ("5645bc057c237b3b69ec1807"),
    "region" : "6001",
    "set_id" : "9",
    "uuid" : "530802b2-22a0-4726-bc4f-a77075568ece",
    "host_id" : "172025008025",
    "host_ip" : "172.25.8.25",
    "create_time" : 20151012,
    "modify_time" : 20151026,
    "cpus" : 2,
    "deleted" : 1,
    "type" : 100,
    "saveTime" : 20151113,
    "inner_member" : 1,
    "__v" : 0,
    "user_email" : "uhosttest@ucloud.cn",
    "company_id" : 23313,
    "company_name" : "基础云计算中心",
    "top_organization_id" : 23313,
    "uhost_instance" : {
        "os_name" : "CentOS 6.5 64位",
        "disks" : 20,
        "memory" : 2048,
        "cpus" : 2
    },
    "industry_type" : "企业服务（SAAS/PAAS）"
}