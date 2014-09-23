from datetime import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import force_unicode

from caching.base import CachingManager, CachingMixin
import requests
from sorl.thumbnail import ImageField
from source.utils.caching import expire_page_cache

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
    twitter_bio = models.TextField(blank=True)
    twitter_profile_image_url = models.URLField(verify_exists=False, blank=True)
    github_username = models.CharField(max_length=32, blank=True)
    github_repos_num = models.PositiveIntegerField(blank=True, null=True)
    github_gists_num = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField('Bio', blank=True)
    organizations = models.ManyToManyField('Organization', blank=True, null=True)
    objects = models.Manager()
    live_objects = LivePersonManager()
    
    class Meta:
        ordering = ('last_name', 'first_name',)
        verbose_name_plural = 'People'
        
    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)
        
    def save(self, *args, **kwargs):
        # clean up our username fields, just in case
        if self.twitter_username:
            self.twitter_username = self.twitter_username.strip()
            if self.twitter_username.startswith('@'):
                self.twitter_username = self.twitter_username.strip('@')
            if '/' in self.twitter_username:
                self.twitter_username = self.twitter_username.split('/')[-1]
        if self.github_username:
            self.github_username = self.github_username.strip()
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

    def get_live_article_set(self):
        return self.article_set.filter(is_live=True, show_in_lists=True, pubdate__lte=datetime.now)

    def get_live_article_authored_set(self):
        return self.article_authors.filter(is_live=True, show_in_lists=True, pubdate__lte=datetime.now)

    def get_live_organization_set(self):
        return self.organizations.filter(is_live=True)

    def get_live_code_set(self):
        return self.code_set.filter(is_live=True)


class PersonLink(CachingMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    person = models.ForeignKey(Person)
    name = models.CharField(max_length=128)
    url = models.URLField(verify_exists=False)
    objects = models.Manager()

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
    email = models.EmailField('Email address', blank=True)
    twitter_username = models.CharField(max_length=32, blank=True)
    github_username = models.CharField(max_length=32, blank=True)
    github_repos_num = models.PositiveIntegerField(blank=True, null=True)
    github_gists_num = models.PositiveIntegerField(blank=True, null=True)
    homepage = models.URLField(verify_exists=False, blank=True)
    description = models.TextField(blank=True)
    # Location
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=32, blank=True)
    country = models.CharField(max_length=32, blank=True, help_text="Only necessary if outside the U.S.")
    logo = ImageField(upload_to='img/uploads/org_logos', help_text="Resized to fit 200x50 box in template", blank=True, null=True)
    objects = models.Manager()
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
        
    def get_live_article_set(self):
        return self.article_set.filter(is_live=True, show_in_lists=True, pubdate__lte=datetime.now)
        
    def get_live_person_set(self):
        return self.person_set.filter(is_live=True)

    def get_live_code_set(self):
        return self.code_set.filter(is_live=True)


class OrganizationLink(CachingMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey(Organization)
    name = models.CharField(max_length=128)
    url = models.URLField(verify_exists=False)
    objects = models.Manager()

    class Meta:
        ordering = ('organization', 'name',)
        verbose_name = 'Organization Link'

    def __unicode__(self):
        return u'%s: %s' % (self.organization.name, self.name)


@receiver(post_save, sender=Person)
def clear_caches_for_person(sender, instance, **kwargs):
    # clear cache for person detail page
    expire_page_cache(instance.get_absolute_url())

    # clear cache for person list page
    expire_page_cache(reverse('person_list'))

    # clear caches for related articles
    for article in instance.get_live_article_set():
        expire_page_cache(article.get_absolute_url())
        if article.section.slug:
            expire_page_cache(reverse(
                'article_list_by_section',
                kwargs = { 'section': article.section.slug }
            ))
        if article.category:
            expire_page_cache(reverse(
                'article_list_by_category',
                kwargs = { 'category': article.category.slug }
            ))

    for article in instance.get_live_article_authored_set():
        expire_page_cache(article.get_absolute_url())
        if article.section.slug:
            expire_page_cache(reverse(
                'article_list_by_section',
                kwargs = { 'section': article.section.slug }
            ))
        if article.category:
            expire_page_cache(reverse(
                'article_list_by_category',
                kwargs = { 'category': article.category.slug }
            ))

    # clear caches for related organizations
    for organization in instance.get_live_organization_set():
        expire_page_cache(organization.get_absolute_url())

    # clear caches for related code index entries
    for code in instance.get_live_code_set():
        expire_page_cache(code.get_absolute_url())


@receiver(post_save, sender=Organization)
def clear_caches_for_organization(sender, instance, **kwargs):
    # clear cache for organization detail page
    expire_page_cache(instance.get_absolute_url())

    # clear cache for organization list page
    expire_page_cache(reverse('organization_list'))

    # clear caches for related articles
    for article in instance.get_live_article_set():
        expire_page_cache(article.get_absolute_url())
        if article.section.slug:
            expire_page_cache(reverse(
                'article_list_by_section',
                kwargs = { 'section': article.section.slug }
            ))
        if article.category:
            expire_page_cache(reverse(
                'article_list_by_category',
                kwargs = { 'category': article.category.slug }
            ))

    # clear caches for related people
    for person in instance.get_live_person_set():
        expire_page_cache(person.get_absolute_url())

    # clear caches for related code index entries
    for code in instance.get_live_code_set():
        expire_page_cache(code.get_absolute_url())
