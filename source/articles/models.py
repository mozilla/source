from datetime import datetime

from django.db import models
from django.template.defaultfilters import date as dj_date, linebreaks

import caching.base
from source.people.models import Person, Organization
from source.code.models import Code
from taggit.managers import TaggableManager


ARTICLE_TYPE_CHOICES = (
    ('project', 'Project'),
    ('tool', 'Tool'),
    ('how-to', 'How-To'),
    ('interview', 'Interview'),
    ('roundtable', 'Roundtable'),
    ('roundup', 'Roundup'),
    ('event', 'Event'),
    ('update', 'Community Update'),
)

class LiveArticleManager(caching.base.CachingManager):
    def get_query_set(self):
        return super(LiveArticleManager, self).get_query_set().filter(is_live=True, pubdate__lte=datetime.now())

class Article(caching.base.CachingMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_live = models.BooleanField('Display on site', default=True)
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    pubdate = models.DateTimeField(default=datetime.now)
    subhead = models.CharField(max_length=128)
    authors = models.ManyToManyField(Person, blank=True, null=True, related_name='article_authors')
    body = models.TextField()
    summary = models.TextField()
    article_type = models.CharField(max_length=32, choices=ARTICLE_TYPE_CHOICES, blank=True)
    people = models.ManyToManyField(Person, blank=True, null=True)
    organizations = models.ManyToManyField(Organization, blank=True, null=True)
    code = models.ManyToManyField(Code, blank=True, null=True)
    tags = TaggableManager(blank=True)
    objects = caching.base.CachingManager()
    live_objects = LiveArticleManager()
    
    class Meta:
        ordering = ('-pubdate','title',)
        
    def __unicode__(self):
        return '%s' % self.title
        
    @models.permalink
    def get_absolute_url(self):
        return ('article_detail', (), {
            'slug': self.slug })
            
    @property
    def pretty_pubdate(self):
        return dj_date(self.pubdate,"F j, Y")
        

class ArticleBlock(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(Article)
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=1)
    body = models.TextField()
    
    class Meta:
        ordering = ('article', 'order', 'title',)
        verbose_name = 'Article Block'

    def __unicode__(self):
        return '%s: %s' % (self.article.title, self.title)


