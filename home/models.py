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


class T_db_instance(Document):
    DBId = StringField()
    InstanceMode = StringField()
    ClusterId = StringField()
    Role = StringField()
    State = StringField()
    DBType = StringField()
    CreateTime = IntField()
    ModifyTime = DateTimeField()
    DiskType = StringField()
    DiskSpace = IntField()
    MemoryLimit = IntField()
    Industry = StringField()
    Manager = StringField()
    CompanyName = StringField()
    CompanyId = StringField()
    InnerMakr = StringField()
