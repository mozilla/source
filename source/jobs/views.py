from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView

from .models import Job


class JobList(ListView):
    model = Job

    def dispatch(self, *args, **kwargs):
        self.render_json = kwargs.get('render_json', False)
        return super(JobList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = Job.live_objects.all()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(JobList, self).get_context_data(**kwargs)
        context['active_nav'] = 'Jobs'

        #context['rss_link'] = reverse('code_list_feed')
        #context['json_link'] = reverse('code_list_feed_json')
        
        return context
