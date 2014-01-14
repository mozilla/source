from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView

from .models import Job
from source.base.helpers import dj_date
from source.base.utils import render_json_to_response


class JobList(ListView):
    model = Job

    def dispatch(self, *args, **kwargs):
        self.render_json = kwargs.get('render_json', False)
        return super(JobList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = Job.live_objects.order_by('-listing_start_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super(JobList, self).get_context_data(**kwargs)
        context['active_nav'] = 'Jobs'

        context['rss_link'] = reverse('job_list_feed')
        context['json_link'] = reverse('job_list_feed_json')
        
        return context

    def render_to_response(self, context):
        if self.render_json:
            jobs = []
            for job in context['object_list']:
                jobs.append({
                    'name': job.name,
                    'organization': job.organization.name,
                    'listed': dj_date(job.listing_start_date, 'F j, Y'),
                })
            return render_json_to_response(jobs)
        return super(JobList, self).render_to_response(context)
