# coding:utf8
from functools import wraps
from django.http import JsonResponse

__author__ = 'kevin'


def ajax_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        json = {'is_authenticated': False}
        return JsonResponse(json)
    return wrapper
