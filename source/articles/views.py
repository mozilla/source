from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Article
from source.base.utils import paginate
from taggit.models import Tag

# Current iteration does not use this in nav, but leaving dict
# in place for feed, url imports until we make a permanent call
SECTION_MAP = {
    'articles': {
        'name': 'Features', 
        'slug': 'articles',
        'article_types': ['project', 'tool', 'how-to', 'interview', 'roundtable', 'roundup', 'event', 'update'],
    },
    'learning': {
        'name': 'Learning', 
        'slug': 'learning',
        'article_types': ['learning',],
    },
}

# Current iteration only has *one* articles section, but this map is in place
# in case we split out into multiple sections that need parent categories
CATEGORY_MAP = {
    'project': {
        'name': 'Project',
        'parent_name': 'Features',
        'parent_slug': 'articles',
    },
    'tool': {
        'name': 'Tool',
        'parent_name': 'Features',
        'parent_slug': 'articles',
    },
    'how-to': {
        'name': 'How-to',
        'parent_name': 'Features',
        'parent_slug': 'articles',
    },
    'interview': {
        'name': 'Interview',
        'parent_name': 'Features',
        'parent_slug': 'articles',
    },
    'roundtable': {
        'name': 'Roundtable',
        'parent_name': 'Features',
        'parent_slug': 'articles',
    },
    'roundup': {
        'name': 'Roundup',
        'parent_name': 'Features',
        'parent_slug': 'articles',
    },
    'event': {
        'name': 'Event',
        'parent_name': 'Features',
        'parent_slug': 'articles',
    },
    'update': {
        'name': 'Update',
        'parent_name': 'Features',
        'parent_slug': 'articles',
    },
    'learning': {
        'name': 'Learning',
        'parent_name': 'Learning',
        'parent_slug': 'learning',
    },
}

class ArticleList(ListView):
    model = Article

    def dispatch(self, *args, **kwargs):
        self.section = kwargs.get('section', None)
        self.category = kwargs.get('category', None)
        self.tags = None
        self.tag_slugs = kwargs.get('tag_slugs', None)
        self.tag_slug_list = []
        return super(ArticleList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = Article.live_objects.prefetch_related('authors', 'people', 'organizations')

        if self.section:
            queryset = queryset.filter(article_type__in=SECTION_MAP[self.section]['article_types'])
        elif self.category:
            queryset = queryset.filter(article_type=self.category)
        elif self.tag_slugs:
            self.tag_slug_list = self.tag_slugs.split('+')
            # need to fail if any item in slug list references nonexistent tag
            self.tags = [get_object_or_404(Tag, slug=tag_slug) for tag_slug in self.tag_slug_list]
            for tag_slug in self.tag_slug_list:
                queryset = queryset.filter(tags__slug=tag_slug)
            
        return queryset
    
    def get_section_links(self, context):
        if self.section:
            context.update({
                'section': SECTION_MAP[self.section],
                'active_nav': SECTION_MAP[self.section]['slug'],
                'rss_link': reverse('article_list_by_section_feed', kwargs={'section': self.section}),
            })
        elif self.category:
            context.update({
                'category': CATEGORY_MAP[self.category]['name'],
                'section': SECTION_MAP[CATEGORY_MAP[self.category]['parent_slug']],
                'active_nav': CATEGORY_MAP[self.category]['parent_slug'],
                'rss_link': reverse('article_list_by_category_feed', kwargs={'category': self.category}),
            })
        elif self.tags:
            context.update({
                'section': SECTION_MAP['articles'],
                'active_nav': SECTION_MAP['articles']['slug'],
                'tags':self.tags,
                'rss_link': reverse('article_list_by_tag_feed', kwargs={'tag_slugs': self.tag_slugs}),
            })
        else:
            context.update({
                'rss_link': reverse('homepage_feed'),
            })
        
        return ''

    def paginate_list(self, context):
        page, paginator = paginate(self.request, self.object_list, 20)
        context.update({
            'page': page,
            'paginator': paginator
        })
        
        return ''
        
    def get_standard_context(self, context):
        self.get_section_links(context)
        self.paginate_list(context)
        
        return ''
        
    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        self.get_standard_context(context)
        
        return context


class ArticleDetail(DetailView):
    model = Article

    def get_queryset(self):
        if self.request.user.is_staff:
            # simple method for allowing article preview for editors,
            # bypassing `live_objects` check on detail view. List pages
            # populate with public articles only, but admin user can hit
            # "view on site" button to see article even if it's not live yet
            queryset = Article.objects.all()
        else:
            queryset = Article.live_objects.all()
            
        queryset = queryset.prefetch_related('articleblock_set', 'authors', 'people', 'organizations', 'code')
        
        return queryset

