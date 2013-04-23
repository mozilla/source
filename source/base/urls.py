from django.conf import settings
from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page

from .feeds import ArticleFeed
from .views import SourceSearchView, HomepageView
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory
from source.articles.models import CATEGORY_MAP, SECTION_MAP
from source.articles.views import ArticleList, ArticleDetail
from source.utils.caching import ClearCache

article_section_options = "|".join(SECTION_MAP.keys())
article_category_options = "|".join(CATEGORY_MAP.keys())
STANDARD_CACHE_TIME = getattr(settings, 'CACHE_MIDDLEWARE_SECONDS', 60*15)
FEED_CACHE_TIME = getattr(settings, 'FEED_CACHE_SECONDS', 60*15)

urlpatterns = patterns('',
    url(
        regex = '^$',
        view = cache_page(HomepageView.as_view(template_name='homepage.html'), STANDARD_CACHE_TIME),
        kwargs = {},
        name = 'homepage',
    ),
    url(
        regex = '^rss/$',
        view = cache_page(ArticleFeed(), FEED_CACHE_TIME),
        kwargs = {},
        name = 'homepage_feed',
    ),
    # matching /articles/ here to offer future support for multiple sections
    url(
        regex = '^(?P<section>%s)/$' % article_section_options,
        view = cache_page(ArticleList.as_view(), STANDARD_CACHE_TIME),
        kwargs = {},
        name = 'article_list_by_section',
    ),
    url(
        regex = '^(?P<section>%s)/rss/$' % article_section_options,
        view = cache_page(ArticleFeed(), FEED_CACHE_TIME),
        kwargs = {},
        name = 'article_list_by_section_feed',
    ),
    url(
        regex = '^(?P<section>%s)/(?P<slug>[-\w]+)/$' % article_section_options,
        view = cache_page(ArticleDetail.as_view(), STANDARD_CACHE_TIME),
        kwargs = {},
        name = 'article_detail',
    ),
    url(
        regex = '^category/(?P<category>%s)/$' % article_category_options,
        view = cache_page(ArticleList.as_view(), STANDARD_CACHE_TIME),
        kwargs = {},
        name = 'article_list_by_category',
    ),
    url(
        regex = '^category/(?P<category>%s)/rss/$' % article_category_options,
        view = cache_page(ArticleFeed(), FEED_CACHE_TIME),
        kwargs = {},
        name = 'article_list_by_category_feed',
    ),
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
    (r'^articles/', include('source.articles.urls')),
    (r'^code/', include('source.code.urls')),
    (r'^people/', include('source.people.urls.people')),
    (r'^organizations/', include('source.people.urls.organizations')),
)
