from datetime import datetime, timedelta

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import date as dj_date, slugify
from django.utils.safestring import mark_safe

from caching.base import CachingManager, CachingMixin
from sorl.thumbnail import ImageField
from source.people.models import Organization
from source.utils.caching import expire_page_cache

def get_today():
    return datetime.now().date()
    
def get_today_plus_30():
    return datetime.now().date() + timedelta(days=30)
    
class LiveJobManager(CachingManager):
    def get_query_set(self):
        today = get_today()
        return super(LiveJobManager, self).get_query_set().filter(
            is_live=True, listing_start_date__lte=today, listing_end_date__gte=today
        )

class Job(CachingMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_live = models.BooleanField('Display on site', default=True, help_text='Job will display if this is checked and dates are within proper range')
    organization = models.ForeignKey(Organization, blank=True, null=True)
    name = models.CharField('Job name', max_length=128)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    listing_start_date = models.DateField(default=get_today)
    listing_end_date = models.DateField(default=get_today_plus_30)
    tweeted_at = models.DateTimeField(blank=True, null=True)
    url = models.URLField(blank=True, null=True, verify_exists=False)
    contact_name = models.CharField('Contact name', max_length=128, blank=True)
    email = models.EmailField('Contact email', blank=True)
    location = models.CharField('Job location', max_length=128, blank=True)
    objects = models.Manager()
    live_objects = LiveJobManager()
    
    class Meta:
        ordering = ('organization','slug',)
    
    def __unicode__(self):
        return u'%s: %s' % (self.name, self.organization)

    def will_show_on_site(self):
        today = get_today()
        return (self.is_live and self.listing_start_date <= today and self.listing_end_date >= today)
    will_show_on_site.boolean = True

    @property
    def get_list_page_url(self):
        return '%s%s#job-%s' % (settings.BASE_SITE_URL, reverse('job_list'), self.pk)

    @property
    def organization_sort_name(self):
        return self.organization.name.replace('The ', '')

    @property
    def get_contact_email(self):
        '''returns job email, falls back to organzation email'''
        return self.email or self.organization.email
    
    @property
    def pretty_start_date(self):
        '''pre-process for simpler template logic'''
        return dj_date(self.listing_start_date,"F j, Y")
        
    @property
    def wrapped_job_name(self):
        if self.url:
            link = '<a class="job-name" href="%s">%s</a>' % (self.url, self.name)
            return mark_safe(link)
        else:
            return self.name

    @property
    def wrapped_organization_name(self):
        if self.organization.is_live and self.organization.show_in_lists:
            link = '<a class="job-organization" href="%s">%s</a>' % (self.organization.get_absolute_url(), self.organization.name)
            return mark_safe(link)
        else:
            return self.organization.name

    @property
    def wrapped_contact_name(self):
        if self.get_contact_email:
            name = self.contact_name or 'Email'
            link = '<a href="mailto:%s">%s</a>' % (self.get_contact_email, name)
            return mark_safe(link)
        else:
            name = self.contact_name or ''
            return name

    def save(self, *args, **kwargs):
        '''prepend pk to job slug to keep things unique'''
        # save so we have a pk for new records
        if not self.pk:
            super(Job, self).save(*args, **kwargs)

        # if we're resaving an existing record, strip the pk
        # off the front so we don't end up multiplying them
        slug_prefix = '%s-' % self.pk
        if self.slug.startswith(slug_prefix):
            self.slug = self.slug.replace(slug_prefix, '')
            
        if self.slug == '':
            self.slug = slugify(self.name)[:40]
        
        # prefix with pk
        self.slug = '%s%s' % (slug_prefix, self.slug)

        # call this manually because of the double-save for slugging
        clear_caches_for_job(self)

        super(Job, self).save(*args, **kwargs)

def clear_caches_for_job(instance):
    '''
    Not triggering this via signal, as we seemed to have
    trouble getting consistent results with the double-save
    required for a unique slug. Called manually instead.
    '''
    # clear cache for job list page
    expire_page_cache(reverse('job_list'))

    # clear caches for related organization
    if instance.organization:
        expire_page_cache(instance.organization.get_absolute_url())
