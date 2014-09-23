from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.models import modelformset_factory
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.views.generic import ListView, DetailView, View

from .forms import OrganizationUpdateForm, PersonUpdateForm
from .models import Person, Organization

from source.utils.json import render_json_to_response

USER_DEBUG = getattr(settings, 'USER_DEBUG', False)


class PersonList(ListView):
    model = Person

    def get_queryset(self):
        queryset = Person.live_objects.exclude(show_in_lists=False).prefetch_related('organizations')
        
        return queryset

class PersonDetail(DetailView):
    model = Person

    def get_queryset(self):
        queryset = Person.live_objects.prefetch_related('personlink_set', 'organizations', 'code_set', 'article_set', 'article_authors')
        
        return queryset
        
class PersonSearchJson(View):
    def get_queryset(self):
        queryset = Person.live_objects.exclude(show_in_lists=False)
        
        return queryset

    def get(self, request, *args, **kwargs):
        people = self.get_queryset()

        q = self.request.GET.get('q', None)
        if 'q' in self.request.GET:
            people = people.filter(Q(first_name__icontains = q) | Q(last_name__icontains = q))
            
        people = people.values('first_name', 'last_name', 'email', 'twitter_username', 'github_username', 'id')
        for person in list(people):
            person['name'] = '%s %s' % (person['first_name'], person['last_name'])

        return render_json_to_response(list(people))

class OrganizationList(ListView):
    model = Organization

    def get_queryset(self):
        queryset = Organization.live_objects.exclude(show_in_lists=False).all()
        
        return queryset

class OrganizationDetail(DetailView):
    model = Organization

    def get_queryset(self):
        queryset = Organization.live_objects.prefetch_related('organizationlink_set')
        
        return queryset

class PersonUpdate(View):
    template_name = "people/person_update.html"
    form_message = ''
    
    def get_success_url(self):
        return reverse('person_update')

    def get_organization(self):
        user = self.request.user
        if user.is_authenticated() and user.is_active:
            organization = get_object_or_404(Organization, is_live=True, email=user.email)
            return organization
        elif USER_DEBUG:
            organization = get_object_or_404(Organization, is_live=True, slug='spokesman-review')
            return organization
        return None

    def get_person(self, pk=None, organization=None, task=None):
        user = self.request.user
        if USER_DEBUG or (user.is_authenticated() and user.is_active):
            if pk and organization:
                # allow for 'add' task
                if task == 'add':
                    person = get_object_or_404(Person, is_live=True, pk=pk)
                else:
                    # ensure that Organization admin can modify this record
                    person = get_object_or_404(Person, is_live=True, pk=pk, organizations=organization)
            else:
                # or that the authenticated user *is* this person
                person = get_object_or_404(Person, is_live=True, email=user.email)
            return person
        return None
        
    def create_person(self, data, organization):
        name = data['name']
        # make sure we actually have been given a name
        if name:
            try:
                first_name, last_name = name.split(' ', 1)
            except:
                first_name, last_name = name, ''
                
            person_kwargs = {
                'first_name': first_name,
                'last_name': last_name,
                'slug': slugify('-'.join([first_name, last_name]))
            }

            i = 0
            found = True
            while found:
                i += 1
                try:
                    person = Person.objects.get(slug=person_kwargs['slug'])
                    person_kwargs['slug'] = slugify('-'.join([first_name, last_name, str(i)]))
                except ObjectDoesNotExist:
                    person = Person(**person_kwargs)
                    person.save()
                    person.organizations.add(organization)
                    found = False
            
            return person
        return None

    def process_form(self, person, data):
        person_form = PersonUpdateForm(instance=person, data=data)
        if person_form.is_valid():
            person_form.save()
            form_message = 'Saved!'
        else:
            error_message = ''
            for field in person_form:
                if field.errors:
                    add_label = field.label
                    add_errors = ', '.join([error for error in field.errors])
                    error_message += '%s: %s ' % (add_label, add_errors)
            form_message = error_message

        return form_message
        
    def post(self, request, *args, **kwargs):
        data = request.POST
        form_message = ''
        success_url = self.get_success_url()
        
        if 'organization_task' in data:
            success_url = reverse('organization_update')
            self.template_name = "people/organization_update.html"
            task = data['organization_task']
            organization = self.get_organization()
            
            if task == 'create':
                person = self.create_person(data, organization)
                form_message = 'Created'
                success_url += '?new=%s' % person.pk
            else:
                person = self.get_person(data['person'], organization, task)
                if task == 'update':
                    form_message = self.process_form(person, data)
                elif task == 'remove':
                    person.organizations.remove(organization)
                    form_message = 'Removed'
                elif task == 'add':
                    person.organizations.add(organization)
                    form_message = 'Added'
        else:
            person = self.get_person()
            form_message = self.process_form(person, data)
        
        if request.is_ajax():
            result = {
                'message': form_message,
                'person': {
                    'name': person.name(),
                    'pk': person.pk,
                    'first_name': person.first_name,
                    'last_name': person.last_name,
                    'email': person.email,
                    'twitter_username': person.twitter_username,
                    'github_username': person.github_username
                }
            }
            return render_json_to_response(result)

        # if for some reason we're not hitting via ajax
        messages.success(request, form_message)
        return redirect(success_url)
    
class OrganizationUpdate(View):
    template_name = "people/organization_update.html"
    error_message = ""
    
    def get_organization(self, user):
        if user.is_authenticated() and user.is_active:
            try:
                organization = Organization.objects.get(is_live=True, email=user.email)
                return organization
            except Organization.DoesNotExist:
                self.error_message = "No Organization account found that matches the email address used to log in."
            except Organization.MultipleObjectsReturned:
                self.error_message = "Uh-oh, somehow there are multiple Organization accounts attached to this email address. Please contact us for cleanup."
                
        return None

    def get(self, request, *args, **kwargs):
        context = {}
        user = request.user
        
        if user.is_authenticated() and user.is_active:
            organization = self.get_organization(user)
            if organization:
                organization_form = OrganizationUpdateForm(instance=organization)
                context.update({
                    'user': request.user,
                    'organization': organization,
                    'organization_form': organization_form,
                    'default_job_listing_end_date': datetime.today().date() + timedelta(days=30)
                })
            else:
                context.update({
                    'error_message': self.error_message
                })
            
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        context = {}
        user = request.user
        organization = self.get_organization(user)

        if organization:
            organization_form = OrganizationUpdateForm(instance=organization, data=request.POST)
            context.update({
                'user': request.user,
                'organization': organization,
                'organization_form': organization_form,
            })

            if organization_form.is_valid():
                organization_form.save()
                
        if request.is_ajax():
            result = {'success': 'True'}
            return render_json_to_response(result)

        # if for some reason we're not hitting via ajax
        messages.success(request, 'Updates saved')
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))
        
