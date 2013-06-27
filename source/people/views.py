from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView, View

from .forms import OrganizationUpdateForm
from .models import Person, Organization


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

class OrganizationList(ListView):
    model = Organization

    def get_queryset(self):
        queryset = Organization.live_objects.exclude(show_in_lists=False).all()
        
        return queryset

class OrganizationDetail(DetailView):
    model = Organization

    def get_queryset(self):
        queryset = Organization.live_objects.prefetch_related('organizationlink_set', 'person_set', 'code_set', 'article_set')
        
        return queryset

class OrganizationUpdate(View):
    template_name = "people/organization_update.html"
    
    def get_organization(self):
        user = self.request.user
        if user.is_authenticated() and user.is_active:
            organization = get_object_or_404(Organization, is_live=True, email=user.email)
            return organization
        return None

    def get(self, request, *args, **kwargs):
        context = {}
        organization = self.get_organization()
        
        if organization:
            organization_form = OrganizationUpdateForm(instance=organization)
            context.update({
                'user': request.user,
                'organization': organization,
                'organization_form': organization_form,
            })
            
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        context = {}
        organization = self.get_organization()

        if organization:
            organization_form = OrganizationUpdateForm(instance=organization, data=request.POST)
            context.update({
                'user': request.user,
                'organization': organization,
                'organization_form': organization_form,
            })

            if organization_form.is_valid():
                organization_form.save()
                messages.success(request, 'Updated!')
        
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))
        
