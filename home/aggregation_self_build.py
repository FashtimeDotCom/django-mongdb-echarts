from .models import DbSelfBuild


def get_top_10_self_build_instance_count(limit=None):
    pipeline = [
        {
            '$match': {
                'InnerMark': 'No',
            }
        },
        {
            '$project': {
                "CompanyName": "$CompanyName",
                "Province": "$Province",
                "DBClass": "$DBClass",
                "City": "$City",
                "Industry": "$Industry",
                "AzGroup": "$AzGroup",
                "Manager": "$Manager",
            }
        },
        {
            '$group': {
                '_id': "$CompanyName",
                'count': {'$sum': 1},
                'Province': {'$first': "$Province"},
                'City': {'$first': "$City"},
                'DBClass': {'$first': "$DBClass"},
                'Industry': {'$first': "$Industry"},
                'AzGroup': {'$first': "$AzGroup"},
                'manager': {'$first': "$Manager"},
            }
        },
        {
            '$sort': {'count': -1}
        },
        {
            '$limit': limit
        }
    ]
    cur = DbSelfBuild._get_collection().aggregate(pipeline)
    tmp_list = []
    for _ in xrange(0, limit):
        try:
            tmp_list.append(cur.next())
        except StopIteration:
            pass
    cur.close()
    return tmp_list
