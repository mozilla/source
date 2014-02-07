from datetime import datetime
import itertools

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import date as dj_date, linebreaks, removetags

from caching.base import CachingManager, CachingMixin
from sorl.thumbnail import ImageField
from source.code.models import Code
from source.people.models import Person, Organization
from source.tags.models import TechnologyTaggedItem, ConceptTaggedItem
from source.utils.caching import expire_page_cache
from taggit.managers import TaggableManager


class LiveArticleManager(CachingManager):
    def get_query_set(self):
        return super(LiveArticleManager, self).get_query_set().filter(is_live=True, pubdate__lte=datetime.now())

class Article(CachingMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_live = models.BooleanField('Display on site', default=True)
    show_in_lists = models.BooleanField('Show in lists', default=True)
    allow_comments = models.BooleanField('Allow comments', default=True)
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    pubdate = models.DateTimeField(default=datetime.now)
    subhead = models.CharField(max_length=128)
    authors = models.ManyToManyField(Person, blank=True, null=True, related_name='article_authors')
    image = ImageField(upload_to='img/uploads/article_images', help_text='Resized to fit 100% column width in template', blank=True, null=True)
    image_caption = models.TextField(blank=True)
    image_credit = models.CharField(max_length=128, blank=True, help_text='Optional. Will be appended to end of caption in parens. Accepts HTML.')
    body = models.TextField()
    summary = models.TextField()
    article_type = models.CharField(max_length=32, blank=True)
    category = models.ForeignKey('Category')
    people = models.ManyToManyField(Person, blank=True, null=True)
    organizations = models.ManyToManyField(Organization, blank=True, null=True)
    code = models.ManyToManyField(Code, blank=True, null=True)
    tags = TaggableManager(blank=True, help_text='Automatic combined list of Technology Tags and Concept Tags, for easy searching')
    technology_tags = TaggableManager(verbose_name='Technology Tags', help_text='A comma-separated list of tags describing relevant technologies', through=TechnologyTaggedItem, blank=True)
    concept_tags = TaggableManager(verbose_name='Concept Tags', help_text='A comma-separated list of tags describing relevant concepts', through=ConceptTaggedItem, blank=True)
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
            'section': self.section.slug,
            'slug': self.slug
        })
        
    @property
    def section(self):
        '''follow article category through to section'''
        if self.category:
            return self.category.section
        return None
            
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
        
    @property
    def safe_summary(self):
        '''suitable for use in places that must avoid nested anchor tags'''
        return removetags(self.summary, 'a')

    @property
    def merged_tag_list(self):
        '''return a combined list of technology_tags and concept_tags'''
        return [item for item in itertools.chain(self.technology_tags.all(), self.concept_tags.all())]

    def get_live_organization_set(self):
        return self.organizations.filter(is_live=True)

    def get_live_people_set(self):
        return self.people.filter(is_live=True)

    def get_live_author_set(self):
        return self.authors.filter(is_live=True)

    def get_live_code_set(self):
        return self.code.filter(is_live=True)
        
    def get_live_guide_set(self):
        return self.guidearticle_set.filter(guide__is_live=True, guide__show_in_lists=True, guide__pubdate__lte=datetime.now)

    def get_live_author_bio_set(self):
        # only authors with acutal bio information
        author_set = self.get_live_author_set().exclude(description='')
        # filter out bio boxes for Erin, Erika, 
        authors_to_exclude = ['erin-kissane','erika-owens','kio-stark']
        author_set = author_set.exclude(slug__in=authors_to_exclude)
        return author_set


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
    image_credit = models.CharField(max_length=128, blank=True, help_text='Optional. Will be appended to end of caption in parens. Accepts HTML.')
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


@receiver(post_save, sender=Article)
def clear_caches_for_article(sender, instance, **kwargs):
    # clear cache for article detail page
    expire_page_cache(instance.get_absolute_url())
    
    # clear cache for article list pages
    if instance.section.slug:
        expire_page_cache(reverse(
            'article_list_by_section',
            kwargs = { 'section': instance.section.slug }
        ))
    if instance.category:
        expire_page_cache(reverse(
            'article_list_by_category',
            kwargs = { 'category': instance.category.slug }
        ))

    # clear caches for related organizations
    for organization in instance.get_live_organization_set():
        expire_page_cache(organization.get_absolute_url())
        
    # clear caches for related people
    for person in instance.get_live_people_set():
        expire_page_cache(person.get_absolute_url())

    # clear caches for related authors
    for author in instance.get_live_author_set():
        expire_page_cache(author.get_absolute_url())

    # clear caches for related code index entries
    for code in instance.get_live_code_set():
        expire_page_cache(code.get_absolute_url())

    # clear caches for related guides
    for guide in instance.get_live_guide_set():
        expire_page_cache(guide.get_absolute_url())
        
    # clear caches for tag pages. FWIW this will miss
    # tag intersection queries like /foo+bar+baz/, so if we
    # implement those, they may need to expire naturally
    for tag in instance.tags.all():
        expire_page_cache(reverse(
            'article_list_by_tag',
            kwargs = { 'tag_slugs': tag.slug }
        ))


class Section(CachingMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=64)
    slug = models.SlugField()
    description = models.TextField(blank=True, help_text='Optional text to add at top of page. (Shows on promo template only.)')
    gets_promo_items = models.BooleanField(default=False, help_text='Check this to use special template with three promo cards at top.')
    special_template = models.CharField(max_length=255, blank=True)
    objects = models.Manager()
    
    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class Category(CachingMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    section = models.ForeignKey(Section)
    name = models.CharField(max_length=64)
    slug = models.SlugField()
    objects = models.Manager()

    class Meta:
        ordering = ('section', 'name',)
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return u'%s: %s' % (self.section.name, self.name)
