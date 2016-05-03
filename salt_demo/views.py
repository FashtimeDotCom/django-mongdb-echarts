from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from .wraps import ajax_login_required
from SaltStack import SaltStack
from settings.password_settings import _SALT_HOST, _SALT_PORT, _SALT_USER, _SALT_PASS, _SALT_SECURE
# Create your views here.


class IndexView(TemplateView):
    template_name = "salt_demo/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['auther'] = "kevin.gao@ucloud.cn"
        context['current_page'] = "salt_demo"
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)


def is_not_null(arg):
    if arg != 'None' and len(arg) != 0:
        return True
    else:
        return False


def check_cmd(cmd):
    if "rm" not in cmd:
        return True


@ajax_login_required
@csrf_exempt
def cmd_run(request):
    target = request.POST.get('tgt')
    cmd = request.POST.get('cmd')
    if request.is_ajax():
        if is_not_null(target) and is_not_null(cmd):
            if check_cmd(cmd):
                ss = SaltStack(host=_SALT_HOST,
                               port=_SALT_PORT,
                               username=_SALT_USER,
                               password=_SALT_PASS,
                               secure=_SALT_SECURE)
                result = ss.cmd_run(target, cmd)
                data = {
                    'return': result
                }
                return JsonResponse(data, status=200)
            else:
                data = {'return': u"'rm' not supported"}
                return JsonResponse(data, status=400)
        else:
            data = {"return": u"not enough params."}
            return JsonResponse(data, status=400)
    else:
        data = {
            "return": u"nice try."
        }
        return JsonResponse(data, status=400)
