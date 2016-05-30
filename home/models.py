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
    VirtualIP = URLField()
    InstanceMode = StringField()
    ClusterId = StringField()
    Role = StringField()
    SrcDBId = StringField()
    State = StringField()
    DBClass = StringField()
    DBType = StringField()
    CreateTime = DateTimeField()
    DeleteTime = DateTimeField()
    InstanceCycle = IntField()
    CreateDay = IntField()
    DeleteDay = IntField()
    CreateWeek = IntField()
    DeleteWeek = IntField()
    CreateMonth = IntField()
    DeleteMonth = IntField()
    CreateYear = IntField()
    DeleteYear = IntField()
    BusinessCreateDay = IntField()
    BusinessDeleteDay = IntField()
    BusinessCreateWeek = IntField()
    BusinessDeleteWeek = IntField()
    BusinessCreateMonth = IntField()
    BusinessDeleteMonth = IntField()
    BusinessCreateYear = IntField()
    BusinessDeleteYear = IntField()
    DiskType = StringField()
    DiskSpace = IntField()
    MemoryLimit = IntField()
    Industry = StringField()
    Manager = StringField()
    CompanyName = StringField()
    CompanyId = StringField()
    InnerMark = StringField()

    @queryset_manager
    def outer(self, queryset):
        return queryset(Q(State__ne='Delete') & Q(InnerMark='No'))

    @queryset_manager
    def outer_with_delete_and_fail(self, queryset):
        return queryset(Q(InnerMark='No'))

    @queryset_manager
    def outer_all_deleted(self, queryset):
        return queryset(Q(InnerMark='No') & Q(State='Delete'))

    @queryset_manager
    def outer_all(self, queryset):
        return queryset(Q(InnerMark='No'))

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
    VirtualIP = URLField()
    InstanceMode = StringField()
    ClusterId = StringField()
    Role = StringField()
    SrcDBId = StringField()
    State = StringField()
    DBClass = StringField()
    DBType = StringField()
    CreateTime = DateTimeField()
    DeleteTime = DateTimeField()
    InstanceCycle = IntField()
    CreateDay = IntField()
    DeleteDay = IntField()
    CreateWeek = IntField()
    DeleteWeek = IntField()
    CreateMonth = IntField()
    DeleteMonth = IntField()
    CreateYear = IntField()
    DeleteYear = IntField()
    BusinessCreateDay = IntField()
    BusinessDeleteDay = IntField()
    BusinessCreateWeek = IntField()
    BusinessDeleteWeek = IntField()
    BusinessCreateMonth = IntField()
    BusinessDeleteMonth = IntField()
    BusinessCreateYear = IntField()
    BusinessDeleteYear = IntField()
    DiskType = StringField()
    DiskSpace = IntField()
    MemoryLimit = IntField()
    Industry = StringField()
    Manager = StringField()
    CompanyName = StringField()
    CompanyId = StringField()
    InnerMark = StringField()

    @queryset_manager
    def outer(self, queryset):
        return queryset(Q(State__ne='Delete') & Q(InnerMark='No'))

    @queryset_manager
    def outer_with_delete_and_fail(self, queryset):
        return queryset(Q(InnerMark='No'))

    @queryset_manager
    def outer_all_deleted(self, queryset):
        return queryset(Q(InnerMark='No') & Q(State='Delete'))

    @queryset_manager
    def outer_all(self, queryset):
        return queryset(Q(InnerMark='No'))

    @queryset_manager
    def inner(self, queryset):
        return queryset(Q(State__ne='Fail') & Q(State__ne='Delete') & Q(InnerMark='Yes'))

    meta = {
        'collection': 't_ha_instance',
        # 'ordering': ['-ModifyTime'],
    }


class DbSelfBuild(Document):
    Region = StringField()
    AzGroup = StringField()
    DBClass = StringField()
    CreateTime = DateTimeField()
    Industry = StringField()
    CompanyName = StringField()
    Province = StringField()
    Manager = StringField()
    InnerMark = StringField()

    meta = {
        'collection': 't_self_build_instance',
    }

    @queryset_manager
    def outer(self, _queryset):
        return _queryset(Q(State__ne='Delete') & Q(InnerMark='No'))
