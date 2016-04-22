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
    InstanceCycle = IntField()
    CreateTime = DateTimeField()
    ModifyTime = DateTimeField()
    CreateDay = IntField()
    ModifyDay = IntField()
    CreateWeek = IntField()
    ModifyWeek = IntField()
    CreateMonth = IntField()
    ModifyMonth = IntField()
    CreateYear = IntField()
    ModifyYear = IntField()
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
    def outer_with_delete_and_fail(self, queryset):
        return queryset(Q(InnerMark='No'))

    @queryset_manager
    def outer_all_deleted_without_fail(self, queryset):
        return queryset(Q(InnerMark='No') & Q(State__ne='Fail') & Q(State='Delete'))

    @queryset_manager
    def outer_without_fail(self, queryset):
        return queryset(Q(InnerMark='No') & Q(State__ne='Fail'))

    @queryset_manager
    def inner(self, queryset):
        return queryset(Q(State__ne='Fail') & Q(State__ne='Delete') & Q(InnerMark='Yes'))

    meta = {
        'collection': 't_db_instance',
        # 'ordering': ['-ModifyTime'],
    }


class Db_HA(Document):
    Region = StringField()
    AzGroup = StringField()
    DBId = StringField()
    InstanceMode = StringField()
    ClusterId = StringField()
    Role = StringField()
    State = StringField()
    DBClass = StringField()
    DBType = StringField()
    InstanceCycle = IntField()
    CreateTime = DateTimeField()
    ModifyTime = DateTimeField()
    CreateDay = IntField()
    ModifyDay = IntField()
    CreateWeek = IntField()
    ModifyWeek = IntField()
    CreateMonth = IntField()
    ModifyMonth = IntField()
    CreateYear = IntField()
    ModifyYear = IntField()
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
    def outer_with_delete_and_fail(self, queryset):
        return queryset(Q(InnerMark='No'))

    @queryset_manager
    def outer_all_deleted_without_fail(self, queryset):
        return queryset(Q(InnerMark='No') & Q(State__ne='Fail') & Q(State='Delete'))

    @queryset_manager
    def outer_without_delete_without_fail(self, queryset):
        return queryset(Q(InnerMark='No') & Q(State__ne='Fail') & Q(State='Delete'))

    @queryset_manager
    def inner(self, queryset):
        return queryset(Q(State__ne='Fail') & Q(State__ne='Delete') & Q(InnerMark='Yes'))

    meta = {
        'collection': 't_ha_instance',
        # 'ordering': ['-ModifyTime'],
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