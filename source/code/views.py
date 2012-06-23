from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Code
from taggit.models import Tag


class CodeList(ListView):
    model = Code

    def get_queryset(self):
        queryset = Code.objects.filter(is_live=True)
        if 'tag_slug' in self.kwargs:
            queryset = queryset.filter(tags__slug=self.kwargs['tag_slug'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CodeList, self).get_context_data(**kwargs)
        context['active_nav'] = 'Code'
        if 'tag_slug' in self.kwargs:
            context['tag'] = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return context


class CodeDetail(DetailView):
    model = Code