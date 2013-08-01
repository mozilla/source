from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Article, Section, Category
from source.tags.utils import filter_queryset_by_tags
from source.utils.pagination import paginate

class ArticleList(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    section = None
    category = None
    
    def dispatch(self, *args, **kwargs):
        self.section = kwargs.get('section', None)
        if self.section:
            self.section = get_object_or_404(Section, slug=self.section)

        self.category = kwargs.get('category', None)
        if self.category:
            self.category = get_object_or_404(Category, slug=self.category)
            if self.category.slug == 'learning' and not self.section:
                # redirecting this to our "Section" page for Learning
                return HttpResponseRedirect(reverse('article_list_by_section', args=('learning',)))

        self.tag_slugs = kwargs.get('tag_slugs', None)
        self.tags = []
        
        return super(ArticleList, self).dispatch(*args, **kwargs)

    def get_template_names(self):
        template_list = [self.template_name]
        if self.section:
            # check whether template needs promo slots
            if self.section.gets_promo_items:
                template_list.insert(0, 'articles/article_list_with_promos.html')
            # check for template override based on section name
            template_list.insert(0, 'articles/article_list_%s.html' % self.section.name.lower())
            
        return template_list
        
    def get_queryset(self):
        queryset = Article.live_objects.filter(show_in_lists=True).prefetch_related('authors', 'people', 'organizations')

        if self.section:
            queryset = queryset.filter(category__section=self.section)
        elif self.category:
            queryset = queryset.filter(category=self.category)
        elif self.tag_slugs:
            queryset, self.tags = filter_queryset_by_tags(queryset, self.tag_slugs, self.tags)
            
        return queryset
    
    def get_section_links(self, context):
        if self.section:
            context.update({
                'section': self.section,
                'active_nav': self.section.slug,
                'rss_link': reverse('article_list_by_section_feed', kwargs={'section': self.section.slug}),
            })
        elif self.category:
            context.update({
                'category': self.category,
                'section': self.category.section,
                'active_nav': self.category.section.slug,
                'rss_link': reverse('article_list_by_category_feed', kwargs={'category': self.category.slug}),
            })
        elif self.tags:
            context.update({
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
        if self.section and self.section.gets_promo_items:
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
            
        # make sure `section` kwarg matches this article's section
        queryset = queryset.filter(category__section__slug=self.kwargs['section'])

        queryset = queryset.prefetch_related('articleblock_set', 'authors', 'people', 'organizations', 'code')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)

        context.update({
            'section': self.object.section,
        })

        return context
