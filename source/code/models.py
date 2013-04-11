from datetime import datetime
import itertools

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import striptags, truncatewords

from caching.base import CachingManager, CachingMixin
from sorl.thumbnail import ImageField
from source.people.models import Person, Organization
from source.tags.models import TechnologyTaggedItem, ConceptTaggedItem
from source.utils.caching import expire_page_cache
from taggit.managers import TaggableManager


class LiveCodeManager(CachingManager):
    def get_query_set(self):
        return super(LiveCodeManager, self).get_query_set().filter(is_live=True)

class Code(CachingMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_live = models.BooleanField('Display on site', default=True)
    is_active = models.BooleanField('Active project', default=True)
    seeking_contributors = models.BooleanField('Seeking contributors', default=False)
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    url = models.URLField(verify_exists=False)
    description = models.TextField('Description', blank=True)
    summary = models.TextField(blank=True, help_text='Short, one- or two-sentence version of description, used on list pages.')
    screenshot = ImageField(upload_to='img/uploads/code_screenshots', help_text="Resized to fit 350x250 box in template", blank=True, null=True)
    people = models.ManyToManyField(Person, blank=True, null=True)
    organizations = models.ManyToManyField(Organization, blank=True, null=True)
    # adding repo_ fields for future local storage of github data
    repo_last_push = models.DateTimeField(blank=True, null=True)
    repo_forks = models.PositiveIntegerField(blank=True, null=True)
    repo_watchers = models.PositiveIntegerField(blank=True, null=True)
    repo_description = models.TextField(blank=True)
    tags = TaggableManager(blank=True, help_text='Automatic combined list of Technology Tags and Concept Tags, for easy searching')
    technology_tags = TaggableManager(verbose_name='Technology Tags', help_text='A comma-separated list of tags describing relevant technologies', through=TechnologyTaggedItem, blank=True)
    concept_tags = TaggableManager(verbose_name='Concept Tags', help_text='A comma-separated list of tags describing relevant concepts', through=ConceptTaggedItem, blank=True)
    objects = models.Manager()
    live_objects = LiveCodeManager()
    
    class Meta:
        ordering = ('slug',)
        
    def __unicode__(self):
        return u'%s' % self.name
    
    def save(self, *args, **kwargs):
        # GitHub API does not like trailing slashes on repo links
        # so clean things up just in case
        if self.url and 'github.com' in self.url:
            self.url = self.url.rstrip('/')
        super(Code, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('code_detail', (), {
            'slug': self.slug })
            
    @property
    def title(self):
        '''alias for search results template'''
        return self.name

    @property
    def sort_letter(self):
        return self.slug[:1]
        
    @property
    def summary_or_description(self):
        '''for summary on list pages, with fallback to truncated description'''
        if self.summary:
            return self.summary.strip()
        elif self.description:
            _description = striptags(self.description.strip())
            return truncatewords(_description, 25)
        return ''

    @property
    def description_or_summary(self):
        '''for description on detail pages, with fallback to summary'''
        if self.description:
            return self.description.strip()
        elif self.summary:
            return self.summary.strip()
        return ''
        
    @property
    def merged_tag_list(self):
        '''return a combined list of technology_tags and concept_tags'''
        return [item for item in itertools.chain(self.technology_tags.all(), self.concept_tags.all())]

    def get_live_article_set(self):
        return self.article_set.filter(is_live=True, pubdate__lte=datetime.now)

    def get_live_organization_set(self):
        return self.organizations.filter(is_live=True)

    def get_live_people_set(self):
        return self.people.filter(is_live=True)


class CodeLink(CachingMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    code = models.ForeignKey(Code)
    name = models.CharField(max_length=128)
    url = models.URLField(verify_exists=False)
    objects = models.Manager()

    class Meta:
        ordering = ('code', 'name',)
        verbose_name = 'Code Link'

    def __unicode__(self):
        return u'%s: %s' % (self.code.name, self.name)


@receiver(post_save, sender=Code)
def clear_caches_for_code(sender, instance, **kwargs):
    # clear cache for code detail page
    expire_page_cache(instance.get_absolute_url())

    # clear cache for code list page
    expire_page_cache(reverse('code_list'))
    
    # clear cache for homepage
    expire_page_cache(reverse('homepage'))
    
    # clear caches for related articles
    for article in instance.get_live_article_set():
        expire_page_cache(article.get_absolute_url())
        expire_page_cache(reverse(
            'article_list_by_section',
            kwargs = { 'section': article.section['slug'] }
        ))
        expire_page_cache(reverse(
            'article_list_by_category',
            kwargs = { 'category': article.article_type }
        ))

    # clear caches for related organizations
    for organization in instance.get_live_organization_set():
        expire_page_cache(organization.get_absolute_url())

    # clear caches for related people
    for person in instance.get_live_people_set():
        expire_page_cache(person.get_absolute_url())

    # clear caches for tag pages. FWIW this will miss
    # tag intersection queries like /foo+bar+baz/, so if we
    # implement those, they may need to expire naturally
    for tag in instance.tags.all():
        expire_page_cache(reverse(
            'code_list_by_tag',
            kwargs = { 'tag_slugs': tag.slug }
        ))
