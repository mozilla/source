from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView

from .models import Code
from source.base.utils import paginate
from source.tags.models import TechnologyTag, ConceptTag
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
            # need to get actual tag instances, and fail
            # if any item in slug list references nonexistent tag
            self.tags = []
            slugs_checked = []
            slugs_to_check = self.tag_slug_list
            # this isn't pretty, but we need to match multiple tag models
            # so each slug has to be tested against each tag model
            # this is why we cache
            for slug in slugs_to_check:
                for model in [Tag, TechnologyTag, ConceptTag]:
                    try:
                        # see if we have a matching tag
                        found_tag = model.objects.get(slug=slug)
                        # add it to list for page context
                        self.tags.append(found_tag)
                        # remember that we've checked it
                        slugs_checked.append(slug)
                        break
                    except:
                        pass

            # make sure that we found everything we checked for
            if slugs_checked != slugs_to_check:
                raise Http404

            for tag_slug in self.tag_slug_list:
                # Look for matches in both types of tagfields
                # TODO: Remove original `tags` query once content migrates
                # to new split tagfields
                queryset = queryset.filter(Q(tags__slug=tag_slug) | Q(technology_tags__slug=tag_slug) | Q(concept_tags__slug=tag_slug))
                # A record might match multiple tags, but we only want it once
                queryset = queryset.distinct()

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
            if 'callback' in self.request.GET:
                # provide jsonp support for requests
                # with ?callback=foo paramater
                context['jsonp_callback'] = self.request.GET['callback']
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
