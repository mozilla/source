from django.views.generic import ListView, DetailView

from .models import Person, Organization


class PersonList(ListView):
    model = Person

    def get_queryset(self):
        queryset = Person.live_objects.all()
        
        return queryset


class PersonDetail(DetailView):
    model = Person




class OrganizationList(ListView):
    model = Organization

    def get_queryset(self):
        queryset = Organization.live_objects.all()
        
        return queryset


class OrganizationDetail(DetailView):
    model = Organization
