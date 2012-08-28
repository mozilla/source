from django.db import models

from caching.base import CachingManager, CachingMixin
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
    people = models.ManyToManyField(Person, blank=True, null=True)
    organizations = models.ManyToManyField(Organization, blank=True, null=True)
    tags = TaggableManager(blank=True)
    objects = CachingManager()
    live_objects = LiveCodeManager()
    
    class Meta:
        ordering = ('name',)
        
    def __unicode__(self):
        return u'%s' % self.name
        
    @models.permalink
    def get_absolute_url(self):
        return ('code_detail', (), {
            'slug': self.slug })
            
    @property
    def title(self):
        '''alias for search results template'''
        return self.name


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

