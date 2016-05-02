from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .wraps import ajax_login_required
# Create your views here.


class IndexView(TemplateView):
    template_name = "salt_demo/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['auther'] = "kevin.gao@ucloud.cn"
        context['current_page'] = "salt"
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)


@ajax_login_required
def cmdrun(request):
    pass
