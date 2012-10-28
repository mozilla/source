from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from source.articles.models import Article
from source.articles.views import CATEGORY_MAP, SECTION_MAP
from source.code.models import Code
from taggit.models import Tag

class ArticleFeed(Feed):
    def get_object(self, request, *args, **kwargs):
        self.section = kwargs.get('section', None)
        self.category = kwargs.get('category', None)
        self.tag_slug = kwargs.get('tag_slug', None)
        if self.tag_slug:
            self.tag = get_object_or_404(Tag, slug=self.tag_slug)
        return ''

    def title(self, obj):
        if self.section:
            return "Source: %s" % SECTION_MAP[self.section]['name']
        elif self.category:
            return "Source: Articles in the category %s" % CATEGORY_MAP[self.category]['name']
        elif self.tag_slug:
            return "Source: Articles tagged with '%s'" % self.tag.name
        return "Source"

    def link(self, obj):
        if self.section:
            return reverse('article_list_by_section', kwargs={'section': self.section})
        elif self.category:
            return reverse('article_list_by_category', kwargs={'category': self.category})
        elif self.tag_slug:
            return reverse('article_list_by_tag', kwargs={'tag_slug': self.tag_slug})
        return reverse('homepage')

    def description(self, obj):
        identifier = 'from Source'
        if self.section:
            identifier = "in the %s section" % SECTION_MAP[self.section]['name']
        elif self.category:
            identifier = "in the %s category" % CATEGORY_MAP[self.category]['name']
        elif self.tag_slug:
            identifier = "tagged with '%s'" % self.tag.name
        return "Recent articles %s" % identifier

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary
        
    def items(self, obj):
        queryset = Article.live_objects.all()
        if self.section:
            queryset = queryset.filter(article_type__in=SECTION_MAP[self.section]['article_types'])
        elif self.category:
            queryset = queryset.filter(article_type=self.category)
        elif self.tag_slug:
            queryset = queryset.filter(tags__slug=self.tag_slug)
        return queryset[:20]

class CodeFeed(Feed):
    def get_object(self, request, *args, **kwargs):
        self.tags = None
        self.tag_slugs = kwargs.get('tag_slugs', None)
        self.tag_slug_list = []
        if self.tag_slugs:
            self.tag_slug_list = self.tag_slugs.split('+')
            # need to fail if any item in slug list references nonexistent tag
            self.tags = [get_object_or_404(Tag, slug=tag_slug) for tag_slug in self.tag_slug_list]
        return ''

    def title(self, obj):
        identifier = ""
        if self.tags:
            identifier = " tagged '%s'" % "+".join([tag.name for tag in self.tags])
        return "Source: Code%s" % identifier

    def link(self, obj):
        if self.tag_slugs:
            return reverse('code_list_by_tag', kwargs={'tag_slugs': self.tag_slugs})
        return reverse('code_list')

    def description(self, obj):
        identifier = " from Source"
        if self.tag_slugs:
            identifier = " tagged '%s'" % "+".join([tag.name for tag in self.tags])
        return "Recent code index pages%s" % identifier

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def items(self, obj):
        queryset = Code.live_objects.order_by('-created')
        for tag_slug in self.tag_slug_list:
            queryset = queryset.filter(tags__slug=tag_slug)
        return queryset[:20]

