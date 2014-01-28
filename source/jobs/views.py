from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.views.generic import ListView, DetailView, View

from .forms import JobUpdateForm
from .models import Job
from source.base.helpers import dj_date
from source.base.utils import render_json_to_response
from source.people.models import Organization
from source.utils.json import render_json_to_response

USER_DEBUG = getattr(settings, 'USER_DEBUG', False)


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

class JobUpdate(View):
    form_message = ''
    
    def get_success_url(self):
        return reverse('organization_update')
    
    def get_organization(self):
        user = self.request.user
        if user.is_authenticated() and user.is_active:
            organization = get_object_or_404(Organization, is_live=True, email=user.email)
            return organization
        elif USER_DEBUG:
            organization = get_object_or_404(Organization, is_live=True, slug='spokesman-review')
            return organization
        return None

    def get_job(self, pk=None, organization=None, task=None):
        user = self.request.user

        if USER_DEBUG or (user.is_authenticated() and user.is_active):
            if pk and organization:
                # allow for 'add' task
                if task == 'add':
                    job = get_object_or_404(Job, is_live=True, pk=pk)
                else:
                    # ensure that Organization admin can modify this record
                    job = get_object_or_404(Job, is_live=True, pk=pk, organization=organization)
            return job
        return None

    def create_job(self, data, organization):
        # use built-in form validation for new data
        job_form = JobUpdateForm(data=data)
        if job_form.is_valid():
            job_kwargs = job_form.cleaned_data
            job_kwargs.update({
                'organization': organization
            })

            job = Job(**job_kwargs)
            job.save()
            job.slug = '%s-%s' % (job.pk, slugify(job.name))
            job.save()

            return job
        return None

    def process_form(self, job, data):
        job_form = JobUpdateForm(instance=job, data=data)
        if job_form.is_valid():
            job_form.save()
            form_message = 'Saved!'
        else:
            error_message = ''
            for field in job_form:
                if field.errors:
                    add_label = field.label
                    add_errors = ', '.join([error for error in field.errors])
                    error_message += '%s: %s ' % (add_label, add_errors)
            form_message = error_message

        return form_message

    def post(self, request, *args, **kwargs):
        data = request.POST
        form_message = ''
        
        task = data['organization_task']
        organization = self.get_organization()

        if task == 'create':
            job = self.create_job(data, organization)
            form_message = 'Created'
        else:
            job = self.get_job(data['job'], organization, task)
            if task == 'update':
                form_message = self.process_form(job, data)
            elif task == 'remove':
                job.delete()
                form_message = 'Removed'

        if request.is_ajax():
            result = {
                'message': form_message,
                'job': {
                    'name': job.name,
                    'pk': job.pk,
                    'email': job.email,
                    'url': job.url,
                    'listing_end_date': job.listing_end_date
                }
            }
            return render_json_to_response(result)

        # if for some reason we're not hitting via ajax
        messages.success(request, form_message)
        return redirect(self.get_success_url())
