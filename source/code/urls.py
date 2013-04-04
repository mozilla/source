from django.conf import settings
from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic.simple import redirect_to

from .views import CodeList, CodeDetail
from source.base.feeds import CodeFeed

STANDARD_CACHE_TIME = getattr(settings, 'CACHE_MIDDLEWARE_SECONDS', 60*2)
FEED_CACHE_TIME = getattr(settings, 'FEED_CACHE_SECONDS', 60*15)

urlpatterns = patterns('',
    url(
        regex = '^$',
        view = cache_page(CodeList.as_view(), STANDARD_CACHE_TIME),
        kwargs = {},
        name = 'code_list',
    ),
    url(
        regex = '^rss/$',
        view = cache_page(CodeFeed(), FEED_CACHE_TIME),
        kwargs = {},
        name = 'code_list_feed',
    ),
    url(
        regex = '^json/$',
        view = cache_page(CodeList.as_view(), FEED_CACHE_TIME),
        kwargs = {'render_json': True},
        name = 'code_list_feed_json',
    ),
    url(
        regex = '^tags/(?P<tag_slugs>[-\w\+]+)/$',
        view = cache_page(CodeList.as_view(), STANDARD_CACHE_TIME),
        kwargs = {},
        name = 'code_list_by_tag',
    ),
    url(
        regex = '^tags/(?P<tag_slugs>[-\w\+]+)/rss/$',
        view = cache_page(CodeFeed(), FEED_CACHE_TIME),
        kwargs = {},
        name = 'code_list_by_tag_feed',
    ),
    url(
        regex = '^tags/(?P<tag_slugs>[-\w\+]+)/json/$',
        view = cache_page(CodeList.as_view(), FEED_CACHE_TIME),
        kwargs = {'render_json': True},
        name = 'code_list_by_tag_feed_json',
    ),
    url(
        regex = '^tags/$',
        view = redirect_to,
        kwargs  = {'url': '/code/'},
        name = 'code_list_tags',
    ),
    url(
        regex = '^(?P<slug>[-\w]+)/$',
        view = cache_page(CodeDetail.as_view(), STANDARD_CACHE_TIME),
        kwargs = {},
        name = 'code_detail',
    ),
)
