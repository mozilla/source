from django.db import models
from django.utils.encoding import force_unicode

from caching.base import CachingManager, CachingMixin

class LivePersonManager(CachingManager):
    def get_query_set(self):
        return super(LivePersonManager, self).get_query_set().filter(is_live=True)


class Person(CachingMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_live = models.BooleanField('Display on site', default=True)
    show_in_lists = models.BooleanField('Show on People list page', default=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    email = models.EmailField('Email address', blank=True)
    twitter_username = models.CharField(max_length=32, blank=True)
    github_username = models.CharField(max_length=32, blank=True)
    description = models.TextField('Bio', blank=True)
    organizations = models.ManyToManyField('Organization', blank=True, null=True)
    objects = CachingManager()
    live_objects = LivePersonManager()
    
    class Meta:
        ordering = ('last_name', 'first_name',)
        verbose_name_plural = 'People'
        
    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)
        
    def save(self, *args, **kwargs):
        # clean up our username fields, just in case
        if self.twitter_username.startswith('@'):
            self.twitter_username = self.twitter_username.strip('@')
        if '/' in self.twitter_username:
            self.twitter_username = self.twitter_username.split('/')[-1]
        if '/' in self.github_username:
            self.github_username = self.github_username.split('/')[-1]
        super(Person, self).save(*args, **kwargs)

    def name(self):
        return u'%s %s' % (self.first_name, self.last_name)
        
    @models.permalink
    def get_absolute_url(self):
        return ('person_detail', (), {
            'slug': self.slug })
    
    @property
    def sort_letter(self):
        return self.last_name[:1]


class PersonLink(CachingMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    person = models.ForeignKey(Person)
    name = models.CharField(max_length=128)
    url = models.URLField(verify_exists=False)
    objects = CachingManager()

    class Meta:
        ordering = ('person', 'name',)
        verbose_name = 'Person Link'

    def __unicode__(self):
        return u'%s: %s' % (self.person.name, self.name)




class LiveOrganizationManager(CachingManager):
    def get_query_set(self):
        return super(LiveOrganizationManager, self).get_query_set().filter(is_live=True)


class Organization(CachingMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_live = models.BooleanField('Display on site', default=True)
    show_in_lists = models.BooleanField('Show on Organization list page', default=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    twitter_username = models.CharField(max_length=32, blank=True)
    github_username = models.CharField(max_length=32, blank=True)
    homepage = models.URLField(verify_exists=False, blank=True)
    description = models.TextField(blank=True)
    # Location
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=32, blank=True)
    country = models.CharField(max_length=32, blank=True, help_text="Only necessary if outside the U.S.")
    # Images - TODO once we figure out static media storage
    #logo = models.ImageField(upload_to='', blank=True, null=True)
    objects = CachingManager()
    live_objects = LiveOrganizationManager()
    
    class Meta:
        ordering = ('name',)
        
    def __unicode__(self):
        return u'%s' % self.name
        
    def save(self, *args, **kwargs):
        # clean up our username fields, just in case
        if self.twitter_username.startswith('@'):
            self.twitter_username = self.twitter_username.strip('@')
        if '/' in self.twitter_username:
            self.twitter_username = self.twitter_username.split('/')[-1]
        if '/' in self.github_username:
            self.github_username = self.github_username.split('/')[-1]
        super(Organization, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('organization_detail', (), {
            'slug': self.slug })
            
    @property
    def location_string_for_static_map(self):
        _locs = []
        for _loc in [self.address, self.city, self.state, self.country]:
            if _loc: _locs.append(_loc)
        return ",".join(_locs).replace(' ','+')

    @property
    def location_string_city(self):
        _locs = []
        for _loc in [self.city, self.state, self.country]:
            if _loc: _locs.append(_loc)
        return ", ".join(_locs)
        
    @property
    def sort_letter(self):
        return self.name.replace('The ', '')[:1]


class OrganizationLink(CachingMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey(Organization)
    name = models.CharField(max_length=128)
    url = models.URLField(verify_exists=False)
    objects = CachingManager()

    class Meta:
        ordering = ('organization', 'name',)
        verbose_name = 'Organization Link'

    def __unicode__(self):
        return u'%s: %s' % (self.organization.name, self.name)

