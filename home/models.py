# coding:utf8
from __future__ import unicode_literals
from mongoengine import *


class Choice(EmbeddedDocument):
    choice_text = StringField(max_length=200)
    votes = IntField(default=0)


class Poll(Document):
    question = StringField(max_length=200)
    pub_date = DateTimeField(help_text='date published')
    choices = ListField(EmbeddedDocumentField(Choice))


class Db(Document):
    Region = StringField()
    AzGroup = StringField()
    DBId = StringField()
    InstanceMode = StringField()
    ClusterId = StringField()
    Role = StringField()
    State = StringField()
    DBClass = StringField()
    DBType = StringField()
    # CreateTime = StringField()
    CreateTime = DateTimeField()
    # ModifyTime = StringField()
    ModifyTime = DateTimeField()
    CreateWeek = IntField()
    ModifyWeek = IntField()
    CreateMonth = IntField()
    ModifyMonth = IntField()
    DiskType = StringField()
    DiskSpace = IntField()
    MemoryLimit = IntField()
    Industry = StringField()
    Manager = StringField()
    CompanyName = StringField()
    CompanyId = StringField()
    InnerMark = StringField()
    SrcDBId = StringField()
    VirtualIP = URLField()

    @queryset_manager
    def outer(self, queryset):
        return queryset(Q(State__ne='Fail') & Q(State__ne='Delete') & Q(InnerMark='No'))

    @queryset_manager
    def inner(self, queryset):
        return queryset(Q(State__ne='Fail') & Q(State__ne='Delete') & Q(InnerMark='Yes'))

    @queryset_manager
    def top_10_industry(self, queryset):
        return queryset(Q(State__ne='Fail') & Q(State__ne='Delete') & Q(InnerMark='Yes'))

    meta = {
        'collection': 't_db_instance',
        # 'ordering': ['-ModifyTime'],
    }

demo = {
    "Region": "\u5317\u4eacC",
    "AzGroup": "\u5317\u4eac\u4e8c",
    "DBId": "8fa26949-57b4-40e2-a35f-b280dd962805",
    "InstanceMode": "Normal",
    "ClusterId": "",
    "Role": "slave",
    "State": "Shutoff",
    "DBType": "mysql-5.5",
    "CreateTime": "2014-10-16T18:19:40",
    "ModifyTime": "2016-04-15T02:19:50",
    "CreatWeek": 41,
    "ModifyWeek": 15,
    "CreateMonth": 10,
    "ModifyMonth": 4,
    "DiskType": "Normal",
    "DiskSpace": 300,
    "MemoryLimit": 1500,
    "Industry": "\u6e38\u620f",
    "Manager": "chubixin@ucloud.cn",
    "CompanyName": "\u4e0a\u6d77\u4e2d\u6e05\u9f99\u56fe\u7f51\u7edc\u79d1\u6280\u6709\u9650\u516c\u53f8",
    "CompanyId": 6544,
    "InnerMark": "No",

    "SrcDBId": "",
    "VirtualIP": "10.10.24.223",
    "_id": {"$oid": "570fe011023222057a245cda"},
}

"""
date.year、date.month、date.day：年、月、日；
date.replace(year, month, day)：生成一个新的日期对象，用参数指定的年，月，日代替原有对象中的属性。（原有对象仍保持不变）
date.timetuple()：返回日期对应的time.struct_time对象；
date.toordinal()：返回日期对应的Gregorian Calendar日期；
date.weekday()：返回weekday，如果是星期一，返回0；如果是星期2，返回1，以此类推；
data.isoweekday()：返回weekday，如果是星期一，返回1；如果是星期2，返回2，以此类推；
date.isocalendar()：返回格式如(year，month，day)的元组；
date.isoformat()：返回格式如'YYYY-MM-DD’的字符串；
date.strftime(fmt)：自定义格式化字符串。在下面详细讲解。
"""