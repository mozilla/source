from django.views.generic import ListView, DetailView

from .models import Article

SECTION_MAP = {
    'projects': {
        'name': 'Projects', 
        'slug': 'projects',
        'article_types': ['project', 'tool', 'how-to',],
    },
    'community': {
        'name': 'Community', 
        'slug': 'community',
        'article_types': ['interview', 'roundtable', 'roundup', 'event', 'update'],
    },
}

CATEGORY_MAP = {
    'project': {
        'name': 'Project',
        'parent_name': 'Projects',
        'parent_slug': 'projects',
    },
    'tool': {
        'name': 'Tool',
        'parent_name': 'Projects',
        'parent_slug': 'projects',
    },
    'how-to': {
        'name': 'How-to',
        'parent_name': 'Projects',
        'parent_slug': 'projects',
    },
    'interview': {
        'name': 'Interview',
        'parent_name': 'Community',
        'parent_slug': 'community',
    },
    'roundtable': {
        'name': 'Roundtable',
        'parent_name': 'Community',
        'parent_slug': 'community',
    },
    'roundup': {
        'name': 'Roundup',
        'parent_name': 'Community',
        'parent_slug': 'community',
    },
    'event': {
        'name': 'Event',
        'parent_name': 'Community',
        'parent_slug': 'community',
    },
    'update': {
        'name': 'Update',
        'parent_name': 'Community',
        'parent_slug': 'community',
    },
}

class ArticleList(ListView):
    model = Article
    
    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        if self.section:
            context['section'] = SECTION_MAP[self.section]
            context['active_nav'] = SECTION_MAP[self.section]['slug']
        elif self.category:
            context['category'] = CATEGORY_MAP[self.category]['name']
            context['section'] = SECTION_MAP[CATEGORY_MAP[self.category]['parent_slug']]
            context['active_nav'] = CATEGORY_MAP[self.category]['parent_slug']
        return context
    
    def get_queryset(self):
        # TODO add future date filters
        qs = Article.objects.filter(is_live=True)
        self.section = self.kwargs.get('section', None)
        self.category = self.kwargs.get('category', None)
        if self.section:
            qs = qs.filter(article_type__in=SECTION_MAP[self.section]['article_types'])
        elif self.category:
            qs = qs.filter(article_type=self.category)
        return qs


class ArticleDetail(DetailView):
    model = Article

