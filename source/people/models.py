from django.db import models


class LivePersonManager(models.Manager):
    def get_query_set(self):
        return super(LivePersonManager, self).get_query_set().filter(is_live=True)


class Person(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_live = models.BooleanField('Display on site', default=True)
    show_in_lists = models.BooleanField(default=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    email = models.EmailField('Email address', blank=True)
    twitter_username = models.CharField(max_length=32, blank=True)
    github_username = models.CharField(max_length=32, blank=True)
    description = models.TextField('Bio', blank=True)
    organizations = models.ManyToManyField('Organization', blank=True, null=True)
    objects = models.Manager()
    live_objects = LivePersonManager()
    
    class Meta:
        ordering = ('last_name', 'first_name',)
        verbose_name_plural = 'People'
        
    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)
        
    def name(self):
        return '%s %s' % (self.first_name, self.last_name)
        
    @models.permalink
    def get_absolute_url(self):
        return ('person_detail', (), {
            'slug': self.slug })


class PersonLink(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    person = models.ForeignKey(Person)
    name = models.CharField(max_length=128)
    url = models.URLField(verify_exists=False)

    class Meta:
        ordering = ('person', 'name',)
        verbose_name = 'Person Link'

    def __unicode__(self):
        return '%s: %s' % (self.person.name, self.name)




class LiveOrganizationManager(models.Manager):
    def get_query_set(self):
        return super(LiveOrganizationManager, self).get_query_set().filter(is_live=True)


class Organization(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_live = models.BooleanField('Display on site', default=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    twitter_username = models.CharField(max_length=32, blank=True)
    github_username = models.CharField(max_length=32, blank=True)
    description = models.TextField(blank=True)
    # Location
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=32, blank=True)
    country = models.CharField(max_length=32, blank=True)
    # Images - TODO once we figure out static media storage
    #logo = models.ImageField(upload_to='', blank=True, null=True)
    objects = models.Manager()
    live_objects = LiveOrganizationManager()
    
    class Meta:
        ordering = ('name',)
        
    def __unicode__(self):
        return '%s' % self.name
        
    @models.permalink
    def get_absolute_url(self):
        return ('organization_detail', (), {
            'slug': self.slug })


class OrganizationLink(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey(Organization)
    name = models.CharField(max_length=128)
    url = models.URLField(verify_exists=False)

    class Meta:
        ordering = ('organization', 'name',)
        verbose_name = 'Organization Link'

    def __unicode__(self):
        return '%s: %s' % (self.organization.name, self.name)

