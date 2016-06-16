# coding:utf8
from django.contrib.auth.models import User
__author__ = 'kevin'


def check_permission(username, permission):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        email = username + '@ucloud.cn'
        tmp = User.objects.create_user(username=username, email=email)
        tmp.save()
        user = User.objects.get(username=username)
    result = user.has_perm(permission)
    print result
    return result
