from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import date as dj_date, linebreaks, striptags, truncatewords

from caching.base import CachingManager, CachingMixin
from sorl.thumbnail import ImageField
from source.articles.models import Article
from source.utils.caching import expire_page_cache


class LiveGuideManager(CachingManager):
    def get_query_set(self):
        return super(LiveGuideManager, self).get_query_set().filter(is_live=True, show_in_lists=True, pubdate__lte=datetime.now())

class Guide(CachingMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_live = models.BooleanField('Display on site', default=True)
    show_in_lists = models.BooleanField('Show in lists', default=True)
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    pubdate = models.DateTimeField(default=datetime.now)
    image = ImageField(upload_to='img/uploads/guide_images', help_text='Resized to fit 100% column width in template', blank=True, null=True)
    image_caption = models.TextField(blank=True)
    image_credit = models.CharField(max_length=128, blank=True, help_text='Optional. Will be appended to end of caption in parens. Accepts HTML.')
    description = models.TextField('Description', blank=True)
    summary = models.TextField(blank=True, help_text='The two-sentence version of description, to be used on list pages.')
    cover_color = models.CharField(max_length='32', blank=True, help_text='Hex code for background color of title card, e.g. `#256188`. Probably sampled from cover image.')
    objects = models.Manager()
    live_objects = LiveGuideManager()

    class Meta:
        ordering = ('-pubdate','title',)
        
    def __unicode__(self):
        return u'%s' % self.title
        
    @models.permalink
    def get_absolute_url(self):
        return ('guide_detail', (), {
            'slug': self.slug
        })

    @property
    def pretty_pubdate(self):
        '''pre-process for simpler template logic'''
        return dj_date(self.pubdate,"F j, Y")

    @property
    def pretty_caption(self):
        '''pre-process for simpler template logic'''
        _caption = self.image_caption or ''
        _credit = self.image_credit
        if _credit:
            _caption = '%s (%s)' % (_caption, _credit)
        return _caption
        
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
        return self.guidearticle_set.filter(article__is_live=True, article__pubdate__lte=datetime.now)

    def save(self, *args, **kwargs):
        # clean up cover_color field, just in case
        self.cover_color = self.cover_color.strip('#')
        super(Organization, self).save(*args, **kwargs)


class GuideArticle(CachingMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    guide = models.ForeignKey(Guide)
    article = models.ForeignKey(Article)
    order = models.PositiveIntegerField(default=1, blank=True, db_index=True, help_text="A '1' will appear first, a '2' will appear second, and so on.")
    article_notes = models.TextField(blank=True, help_text="Optional field for telling readers why this article is part of this guide.")
    objects = models.Manager()

    class Meta:
        ordering = ('guide', 'order',)
        verbose_name = 'Guide Article'

    def __unicode__(self):
        return u'%s: %s' % (self.guide.title, self.article.title)

    @models.permalink
    def get_absolute_url(self):
        '''shortcut for linking to Guide when GuideArticle is in context'''
        return ('guide_detail', (), {
            'slug': self.guide.slug
        })
        
    @property
    def title(self):
        return self.guide.title


@receiver(post_save, sender=Guide)
def clear_caches_for_guide(sender, instance, **kwargs):
    # clear cache for guide detail page
    expire_page_cache(instance.get_absolute_url())

    # clear cache for guide list page
    expire_page_cache(reverse('guide_list'))

    # clear caches for related articles
    for article in instance.get_live_article_set():
        expire_page_cache(article.article.get_absolute_url())
