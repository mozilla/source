from datetime import datetime, timedelta

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from caching.base import CachingManager, CachingMixin
from sorl.thumbnail import ImageField
from source.people.models import Organization
from source.utils.caching import expire_page_cache

DEFAULT_START = datetime.today().date()
DEFAULT_END = DEFAULT_START + timedelta(days=30)

class LiveJobManager(CachingManager):
    def get_query_set(self):
        return super(LiveJobManager, self).get_query_set().filter(is_live=True)

class Job(CachingMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_live = models.BooleanField('Display on site', default=True)
    organization = models.ForeignKey(Organization, blank=True, null=True)
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    listing_start_date = models.DateField(default=DEFAULT_START)
    listing_end_date = models.DateField(default=DEFAULT_END)
    description = models.TextField(blank=True)
    summary = models.TextField(blank=True, help_text='Short, one- or two-sentence version of description, used on list pages.')
    requirements = models.TextField(blank=True)
    salary = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    job_start_date = models.DateField(blank=True, null=True)
    url = models.URLField(blank=True, null=True, verify_exists=False)
    objects = models.Manager()
    live_objects = LiveJobManager()
    
    class Meta:
        ordering = ('organization','slug',)
        
    def __unicode__(self):
        return u'%s' % self.name
    
    @property
    def summary_or_description(self):
        '''for summary on list pages, with fallback to truncated description'''
        if self.summary:
            return self.summary.strip()
        elif self.description:
            _description = striptags(self.description.strip())
            return truncatewords(_description, 25)
        return ''

    @models.permalink
    def get_absolute_url(self):
        return ('job_detail', (), {
            'slug': self.slug })

@receiver(post_save, sender=Job)
def clear_caches_for_jobs(sender, instance, **kwargs):
    # clear cache for job detail page
    expire_page_cache(instance.get_absolute_url())

    # clear cache for job list page
    expire_page_cache(reverse('job_list'))
    
    # clear caches for related organization
    if instance.organization:
        expire_page_cache(organization.get_absolute_url())
