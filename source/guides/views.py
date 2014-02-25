from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.views.generic import ListView, DetailView

from .models import Guide
from source.utils.json import render_json_to_response


class GuideList(ListView):
    model = Guide

    def dispatch(self, *args, **kwargs):
        self.render_json = kwargs.get('render_json', False)
        return super(GuideList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = Guide.live_objects.all()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(GuideList, self).get_context_data(**kwargs)
        context['active_nav'] = 'Guides'
        context['rss_link'] = reverse('guide_list_feed')

        return context


class GuideDetail(DetailView):
    model = Guide

    def get_queryset(self):
        if self.request.user.is_staff:
            # allow preview for logged-in editors
            queryset = Guide.objects.prefetch_related('guidearticle_set')
        else:
            queryset = Guide.live_objects.prefetch_related('guidearticle_set')
        
        return queryset
