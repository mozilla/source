from datetime import datetime

from django.db import models
from django.template.defaultfilters import date as dj_date, linebreaks

from caching.base import CachingManager, CachingMixin
from sorl.thumbnail import ImageField
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

class LiveArticleManager(CachingManager):
    def get_query_set(self):
        return super(LiveArticleManager, self).get_query_set().filter(is_live=True, pubdate__lte=datetime.now())

class Article(CachingMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_live = models.BooleanField('Display on site', default=True)
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    pubdate = models.DateTimeField(default=datetime.now)
    subhead = models.CharField(max_length=128)
    authors = models.ManyToManyField(Person, blank=True, null=True, related_name='article_authors')
    image = ImageField(upload_to='img/uploads/article_images', help_text='Resized to fit 100% column width in template', blank=True, null=True)
    image_caption = models.TextField(blank=True)
    image_credit = models.CharField(max_length=128, blank=True, help_text='Optional. Will be appended to end of caption in parens.')
    body = models.TextField()
    summary = models.TextField()
    article_type = models.CharField(max_length=32, choices=ARTICLE_TYPE_CHOICES, blank=True)
    people = models.ManyToManyField(Person, blank=True, null=True)
    organizations = models.ManyToManyField(Organization, blank=True, null=True)
    code = models.ManyToManyField(Code, blank=True, null=True)
    tags = TaggableManager(blank=True)
    objects = models.Manager()
    live_objects = LiveArticleManager()
    disable_auto_linebreaks = models.BooleanField(default=False, help_text='Check this if body and article blocks already have HTML paragraph tags.')
    
    class Meta:
        ordering = ('-pubdate','title',)
        
    def __unicode__(self):
        return u'%s' % self.title
        
    @models.permalink
    def get_absolute_url(self):
        return ('article_detail', (), {
            'slug': self.slug })
            
    @property
    def pretty_pubdate(self):
        '''pre-process for simpler template logic'''
        return dj_date(self.pubdate,"F j, Y")

    @property
    def pretty_caption(self):
        '''pre-process for simpler template logic'''
        _caption = self.image_caption or ''
        _credit = self.image_credit
        if _credit:
            _caption = '%s (%s)' % (_caption, _credit)
        return _caption
        
    @property
    def pretty_body_text(self):
        '''pre-process for simpler template logic'''
        _body = self.body
        if not self.disable_auto_linebreaks:
            # allow admin users to provide text
            # that already contains <p> tags
            _body = linebreaks(_body)
        return _body
            

    def get_live_organization_set(self):
        return self.organizations.filter(is_live=True)

    def get_live_people_set(self):
        return self.people.filter(is_live=True)

    def get_live_author_set(self):
        return self.authors.filter(is_live=True)

    def get_live_code_set(self):
        return self.code.filter(is_live=True)


IMAGE_PRESENTATION_CHOICES = (
    ('full-width', 'Full-Width Above Text'),
    ('full-width-below', 'Full-Width Below Text'),
    ('inset-left', 'Inset Left'),
    ('inset-right', 'Inset Right'),
)

class ArticleBlock(CachingMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(Article)
    title = models.CharField(max_length=128)
    slug = models.SlugField()
    order = models.PositiveIntegerField(default=1)
    image = ImageField(upload_to='img/uploads/article_images', blank=True, null=True)
    image_presentation = models.CharField(max_length=24, choices=IMAGE_PRESENTATION_CHOICES, blank=True)
    image_caption = models.TextField(blank=True)
    image_credit = models.CharField(max_length=128, blank=True, help_text='Optional. Will be appended to end of caption in parens.')
    body = models.TextField()
    objects = models.Manager()
    
    class Meta:
        ordering = ('article', 'order', 'title',)
        verbose_name = 'Article Block'

    def __unicode__(self):
        return u'%s: %s' % (self.article.title, self.title)

    @property
    def pretty_caption(self):
        '''pre-process for simpler template logic'''
        _caption = self.image_caption or ''
        _credit = self.image_credit
        if _credit:
            _caption = '%s (%s)' % (_caption, _credit)
        return _caption
        
    @property
    def pretty_body_text(self):
        '''pre-process for simpler template logic'''
        _body = self.body
        if not self.article.disable_auto_linebreaks:
            # allow admin users to provide text
            # that already contains <p> tags
            _body = linebreaks(_body)
        return _body


