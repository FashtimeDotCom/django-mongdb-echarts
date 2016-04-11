from django.shortcuts import render
from .models import Poll, T_db_instance
# Create your views here.
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['asd'] = "123"
        context['current_page'] = "index"
        return context

# for poll in Poll.objects(question__startswith="W"):
for poll in Poll.objects():
    print len(poll.choices),
    print poll.to_json()

T_db_instance(InstanceMode="What is wrong with you?").save()
