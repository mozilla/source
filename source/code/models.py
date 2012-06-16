from django.db import models

from source.people.models import Person, Organization


class Code(models.Model):
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
    #tags
    
    class Meta:
        ordering = ('name',)
        
    def __unicode__(self):
        return '%s' % self.name
        
    @models.permalink
    def get_absolute_url(self):
        return ('code_detail', (), {
            'slug': self.slug })


class CodeLink(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    code = models.ForeignKey(Code)
    name = models.CharField(max_length=128)
    url = models.URLField(verify_exists=False)

    class Meta:
        ordering = ('code', 'name',)
        verbose_name = 'Code Link'

    def __unicode__(self):
        return '%s: %s' % (self.code.name, self.name)

