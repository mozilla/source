from datetime import datetime, timedelta

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from caching.base import CachingManager, CachingMixin
from sorl.thumbnail import ImageField
from source.people.models import Organization
from source.utils.caching import expire_page_cache

TODAY = datetime.today().date()
TODAY_PLUS_30 = TODAY + timedelta(days=30)

class LiveJobManager(CachingManager):
    def get_query_set(self):
        return super(LiveJobManager, self).get_query_set().filter(
            is_live=True, listing_start_date__lte=TODAY, listing_end_date__gte=TODAY
        )

class Job(CachingMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_live = models.BooleanField('Display on site', default=True, help_text='Job will display if this is checked and dates are within proper range')
    organization = models.ForeignKey(Organization, blank=True, null=True)
    name = models.CharField('Job name', max_length=128)
    slug = models.SlugField(unique=True)
    listing_start_date = models.DateField(default=TODAY)
    listing_end_date = models.DateField(default=TODAY_PLUS_30)
    tweeted_at = models.DateTimeField(blank=True, null=True)
    url = models.URLField(blank=True, null=True, verify_exists=False)
    objects = models.Manager()
    live_objects = LiveJobManager()
    
    class Meta:
        ordering = ('organization','slug',)
    
    def __unicode__(self):
        return u'%s: %s' % (self.name, self.organization)
        
    def will_show_on_site(self):
        return (self.is_live and self.listing_start_date <= TODAY and self.listing_end_date >= TODAY)
    will_show_on_site.boolean = True

    def save(self, *args, **kwargs):
        '''prepend pk to job slug to keep things unique'''
        # save so we have a pk for new records
        super(Job, self).save(*args, **kwargs)

        # if we're resaving an existing record, strip the pk
        # off the front so we don't end up multiplying them
        slug_prefix = '%s-' % self.pk
        if self.slug.startswith(slug_prefix):
            self.slug = self.slug.replace(slug_prefix, '')
        
        # prefix with pk
        self.slug = '%s%s' % (slug_prefix, self.slug)

        super(Job, self).save(*args, **kwargs)

@receiver(post_save, sender=Job)
def clear_caches_for_jobs(sender, instance, **kwargs):
    # clear cache for job list page
    expire_page_cache(reverse('job_list'))
    
    # clear caches for related organization
    if instance.organization:
        expire_page_cache(instance.organization.get_absolute_url())
