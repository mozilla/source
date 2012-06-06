from django.views.generic import ListView, DetailView

from source.people.models import Person, Organization


class PersonList(ListView):
    model = Person

    def get_context_data(self, **kwargs):
        context = super(PersonList, self).get_context_data(**kwargs)
        context['active_nav'] = 'People'
        return context


class PersonDetail(DetailView):
    model = Person

    
class OrganizationList(ListView):
    model = Organization

    
class OrganizationDetail(DetailView):
    model = Organization