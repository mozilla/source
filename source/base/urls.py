from django.conf import settings
from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page

from .feeds import ArticleFeed
from .views import SourceSearchView, HomepageView
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory
from source.articles.views import ArticleList, ArticleDetail
from source.utils.caching import ClearCache

STANDARD_CACHE_TIME = getattr(settings, 'CACHE_MIDDLEWARE_SECONDS', 60*15)
FEED_CACHE_TIME = getattr(settings, 'FEED_CACHE_SECONDS', 60*15)

urlpatterns = patterns('',
    url(
        regex = '^$',
        view = cache_page(HomepageView.as_view(template_name='homepage.html'), STANDARD_CACHE_TIME),
        kwargs = {},
        name = 'homepage',
    ),
    (r'^articles/', include('source.articles.urls')),
    (r'^code/', include('source.code.urls')),
    (r'^guides/', include('source.guides.urls')),
    (r'^jobs/', include('source.jobs.urls')),
    (r'^organizations/', include('source.people.urls.organizations')),
    (r'^people/', include('source.people.urls.people')),
    url(
        regex = '^search/$',
        view = search_view_factory(view_class=SourceSearchView, form_class=SearchForm, searchqueryset=SearchQuerySet().order_by('django_ct')),
        kwargs = {},
        name = 'haystack_search',
    ),
    url(
        regex = '^clear-cache/$',
        view = ClearCache.as_view(),
        kwargs = {},
        name = 'clear_cache',
    ),
    url(
        regex = '^rss/$',
        view = cache_page(ArticleFeed(), FEED_CACHE_TIME),
        kwargs = {},
        name = 'homepage_feed',
    ),
    url(
        regex = '^category/(?P<category>[-\w]+)/$',
        view = cache_page(ArticleList.as_view(), STANDARD_CACHE_TIME),
        kwargs = {},
        name = 'article_list_by_category',
    ),
    url(
        regex = '^category/(?P<category>[-\w]+)/rss/$',
        view = cache_page(ArticleFeed(), FEED_CACHE_TIME),
        kwargs = {},
        name = 'article_list_by_category_feed',
    ),
    url(
        regex = '^(?P<section>[-\w]+)/$',
        view = cache_page(ArticleList.as_view(), STANDARD_CACHE_TIME),
        kwargs = {},
        name = 'article_list_by_section',
    ),
    url(
        regex = '^(?P<section>[-\w]+)/rss/$',
        view = cache_page(ArticleFeed(), FEED_CACHE_TIME),
        kwargs = {},
        name = 'article_list_by_section_feed',
    ),
    url(
        regex = '^(?P<section>[-\w]+)/(?P<slug>[-\w]+)/$',
        view = cache_page(ArticleDetail.as_view(), STANDARD_CACHE_TIME),
        kwargs = {},
        name = 'article_detail',
    ),
)
