from django.views.generic import ListView, DetailView

from .models import Person, Organization


class PersonList(ListView):
    model = Person

    def get_queryset(self):
        queryset = Person.live_objects.prefetch_related('organizations')
        
        return queryset


class PersonDetail(DetailView):
    model = Person

    def get_queryset(self):
        queryset = Person.live_objects.prefetch_related('personlink_set', 'organizations', 'code_set', 'article_set', 'article_authors')
        
        return queryset




class OrganizationList(ListView):
    model = Organization

    def get_queryset(self):
        queryset = Organization.live_objects.all()
        
        return queryset


class OrganizationDetail(DetailView):
    model = Organization

    def get_queryset(self):
        queryset = Organization.live_objects.prefetch_related('organizationlink_set', 'person_set', 'code_set', 'article_set')
        
        return queryset
