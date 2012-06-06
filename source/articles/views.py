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

class ArticleList(ListView):
    model = Article
    
    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        section = self.kwargs['section']
        if section:
            context['section'] = SECTION_MAP[section]
            context['active_nav'] = SECTION_MAP[section]['slug']
        return context
    
    def get_queryset(self):
        # TODO add future date filters
        qs = Article.objects.filter(is_live=True)
        section = self.kwargs['section']
        if section:
            qs = qs.filter(article_type__in=SECTION_MAP[section]['article_types'])
        return qs


class ArticleDetail(DetailView):
    model = Article

