from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Article, SECTION_MAP, CATEGORY_MAP
from source.base.utils import paginate
from source.tags.utils import filter_queryset_by_tags

class ArticleList(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    
    def dispatch(self, *args, **kwargs):
        self.section = kwargs.get('section', None)
        self.category = kwargs.get('category', None)
        self.tag_slugs = kwargs.get('tag_slugs', None)
        self.tags = []
        
        if self.category == 'learning' and not self.section:
            # redirecting this to our "Section" page for Learning
            # until we refactor Sections into database models
            return HttpResponseRedirect(reverse('article_list_by_section', args=('learning',)))
        
        if self.section:
            # check for template override based on section name
            self.template_list = [
                'articles/article_list_%s.html' % self.section,
                self.template_name,
            ]
            
        if self.section == 'learning':
            self.template_name = 'articles/article_list_learning.html'
            
        return super(ArticleList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = Article.live_objects.prefetch_related('authors', 'people', 'organizations')

        if self.section:
            queryset = queryset.filter(article_type__in=SECTION_MAP[self.section]['article_types'])
        elif self.category:
            queryset = queryset.filter(article_type=self.category)
        elif self.tag_slugs:
            queryset, self.tags = filter_queryset_by_tags(queryset, self.tag_slugs, self.tags)
            
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
                'tags': self.tags,
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
        
    def get_promo_items(self, context, num_items):
        _page = context.get('page', None)
        
        # Only get promo items for the first page of a paginated section
        if _page and _page.number == 1:
            '''
            Take the most recent three items from this section's list
            of articles. Pop the first item for a `lead_promo` object.
            Stash the rest in a `secondary_promos` list. Also generate
            a set of pks to ignore when we iterate through the main
            headline list.
            '''
            promo_list = self.get_queryset()[:num_items]
            lead_promo = None
            secondary_promos = None
            if promo_list:
                lead_promo = promo_list[0]
                secondary_promos = promo_list[1:]

            context.update({
                'lead_promo': lead_promo,
                'secondary_promos': secondary_promos,
                'articles_to_exclude_from_list': [promo.pk for promo in promo_list]
            })
        
    def get_standard_context(self, context):
        self.get_section_links(context)
        self.paginate_list(context)
        if self.section and SECTION_MAP[self.section]['gets_promo_items']:
            self.get_promo_items(context, 3)
        
        return ''
        
    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        self.get_standard_context(context)
        
        return context


class ArticleDetail(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'

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

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)

        # make sure `section` kwarg matches this article's section
        if self.kwargs['section'] != self.object.section['slug']:
            raise Http404

        context.update({
            'section': self.object.section,
        })

        return context

