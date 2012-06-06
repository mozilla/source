from django.views.generic import ListView, DetailView

from .models import Code


class CodeList(ListView):
    model = Code

    def get_context_data(self, **kwargs):
        context = super(CodeList, self).get_context_data(**kwargs)
        context['active_nav'] = 'Code'
        return context


class CodeDetail(DetailView):
    model = Code