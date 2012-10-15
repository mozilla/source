from datetime import datetime

from django.db import models
from django.template.defaultfilters import striptags, truncatewords

from caching.base import CachingManager, CachingMixin
from sorl.thumbnail import ImageField
from source.people.models import Person, Organization
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
    tags = TaggableManager(blank=True)
    objects = CachingManager()
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
    objects = CachingManager()

    class Meta:
        ordering = ('code', 'name',)
        verbose_name = 'Code Link'

    def __unicode__(self):
        return u'%s: %s' % (self.code.name, self.name)

