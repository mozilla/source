from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404

from source.articles.models import Article
from source.articles.views import CATEGORY_MAP, SECTION_MAP
from source.code.models import Code
from source.tags.models import TechnologyTag, ConceptTag
from taggit.models import Tag

class ObjectWithTagsFeed(Feed):
    '''common get_object for Article and Code feeds to handle tag queries'''
    def get_object(self, request, *args, **kwargs):
        self.section = kwargs.get('section', None)
        self.category = kwargs.get('category', None)
        self.tags = []
        self.tag_slugs = kwargs.get('tag_slugs', None)
        self.tag_slug_list = []
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
        return ''

class ArticleFeed(ObjectWithTagsFeed):
    description_template = "feeds/article_description.html"
    
    def title(self, obj):
        if self.section:
            return "Source: %s" % SECTION_MAP[self.section]['name']
        elif self.category:
            return "Source: Articles in the category %s" % CATEGORY_MAP[self.category]['name']
        elif self.tag_slugs:
            return "Source: Articles tagged with '%s'" % "+".join([tag.name for tag in self.tags])
        return "Source"

    def link(self, obj):
        if self.section:
            return reverse('article_list_by_section', kwargs={'section': self.section})
        elif self.category:
            return reverse('article_list_by_category', kwargs={'category': self.category})
        elif self.tag_slugs:
            return reverse('article_list_by_tag', kwargs={'tag_slugs': self.tag_slugs})
        return reverse('homepage')

    def description(self, obj):
        identifier = 'from Source'
        if self.section:
            identifier = "in the %s section" % SECTION_MAP[self.section]['name']
        elif self.category:
            identifier = "in the %s category" % CATEGORY_MAP[self.category]['name']
        elif self.tag_slugs:
            identifier = "tagged with '%s'" % "+".join([tag.name for tag in self.tags])
        return "Recent articles %s" % identifier

    def item_title(self, item):
        return item.title
        
    def item_pubdate(self, item):
        return item.pubdate
        
    def item_author_name(self, item):
        if item.get_live_author_set().exists():
            return ','.join([author.name() for author in item.get_live_author_set()])
        return ''
        
    def item_categories(self, item):
        if item.article_type:
            return item.get_article_type_display()
        return ''
        
    def items(self, obj):
        queryset = Article.live_objects.all()
        if self.section:
            queryset = queryset.filter(article_type__in=SECTION_MAP[self.section]['article_types'])
        elif self.category:
            queryset = queryset.filter(article_type=self.category)
        elif self.tag_slugs:
            for tag_slug in self.tag_slug_list:
                queryset = queryset.filter(Q(tags__slug=tag_slug) | Q(technology_tags__slug=tag_slug) | Q(concept_tags__slug=tag_slug))
                queryset = queryset.distinct()
        return queryset[:20]

class CodeFeed(ObjectWithTagsFeed):
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
            queryset = queryset.filter(Q(tags__slug=tag_slug) | Q(technology_tags__slug=tag_slug) | Q(concept_tags__slug=tag_slug))
            queryset = queryset.distinct()
        return queryset[:20]

