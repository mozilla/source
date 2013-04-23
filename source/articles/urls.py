from django.conf import settings
from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic.simple import redirect_to

from .views import ArticleList
from source.base.feeds import ArticleFeed

STANDARD_CACHE_TIME = getattr(settings, 'CACHE_MIDDLEWARE_SECONDS', 60*15)
FEED_CACHE_TIME = getattr(settings, 'FEED_CACHE_SECONDS', 60*15)

urlpatterns = patterns('',
    # /articles/ is matched as a section in base.urls
    #url(
    #    regex = '^$',
    #    view = ArticleList.as_view(),
    #    kwargs = {},
    #   name = 'article_list',
    #,
    url(
        regex = '^tags/(?P<tag_slugs>[-\w\+]+)/$',
        view = cache_page(ArticleList.as_view(), STANDARD_CACHE_TIME),
        kwargs = {},
        name = 'article_list_by_tag',
    ),
    url(
        regex = '^tags/(?P<tag_slugs>[-\w\+]+)/rss/$',
        view = cache_page(ArticleFeed(), FEED_CACHE_TIME),
        kwargs = {},
        name = 'article_list_by_tag_feed',
    ),
    url(
        regex = '^tags/$',
        view = redirect_to,
        kwargs  = {'url': '/articles/'},
        name = 'article_list_tags',
    ),
)
