from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView

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

class OrganizationManage(TemplateView):
    template_name = "people/organization_manage.html"
    
    def get_context_data(self, **kwargs):
        context = super(OrganizationManage, self).get_context_data(**kwargs)
        user = self.request.user
        if not user.is_anonymous and user.is_authenticated:
            organization = get_object_or_404(Organization, is_live=True, email=user.email)
            context.update({
                'user': user,
                'organization': organization,
            })

        return context
        