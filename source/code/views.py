from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView

from .models import Code
from source.base.utils import paginate
from taggit.models import Tag


class CodeList(ListView):
    model = Code

    def dispatch(self, *args, **kwargs):
        self.render_json = kwargs.get('render_json', False)
        self.tags = None
        self.tag_slugs = kwargs.get('tag_slugs', None)
        self.tag_slug_list = []
        return super(CodeList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = Code.live_objects.prefetch_related('organizations')

        if self.tag_slugs:
            self.tag_slug_list = self.tag_slugs.split('+')
            # need to fail if any item in slug list references nonexistent tag
            self.tags = [get_object_or_404(Tag, slug=tag_slug) for tag_slug in self.tag_slug_list]
            for tag_slug in self.tag_slug_list:
                queryset = queryset.filter(tags__slug=tag_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(CodeList, self).get_context_data(**kwargs)
        context['active_nav'] = 'Code'

        if self.tags:
            context['tags'] = self.tags
            context['rss_link'] = reverse('code_list_by_tag_feed', kwargs={'tag_slugs': self.tag_slugs})
            context['json_link'] = reverse('code_list_by_tag_feed_json', kwargs={'tag_slugs': self.tag_slugs})
        else:
            context['rss_link'] = reverse('code_list_feed')
            context['json_link'] = reverse('code_list_feed_json')
        
        # No pagination required for current alpha list display
        #page, paginator = paginate(self.request, self.object_list, 50)
        #context.update({
        #    'page': page,
        #    'paginator': paginator
        #})

        return context

    def render_to_response(self, context):
        if self.render_json:
            '''
            JSON export runs through a hand-rolled template for now, so we can
            attach things like related names and urls. If we start doing more
            with providing JSON, we should definitly go full django-tastypie.
            '''
            return render_to_response(
                'code/code_list.json',
                context,
                context_instance = RequestContext(self.request),
                mimetype='application/json'
            )
        return super(CodeList, self).render_to_response(context)


class CodeDetail(DetailView):
    model = Code

    def get_queryset(self):
        queryset = Code.live_objects.prefetch_related('codelink_set', 'people', 'organizations', 'article_set')
        
        return queryset
