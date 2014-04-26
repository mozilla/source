from django.conf import settings
from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page

from .views import GuideList, GuideDetail
from source.base.feeds import GuideFeed

STANDARD_CACHE_TIME = getattr(settings, 'CACHE_MIDDLEWARE_SECONDS', 60*15)
FEED_CACHE_TIME = getattr(settings, 'FEED_CACHE_SECONDS', 60*15)

urlpatterns = patterns('',
    url(
        regex = '^$',
        view = cache_page(GuideList.as_view(), STANDARD_CACHE_TIME),
        kwargs = {},
        name = 'guide_list',
    ),
    url(
        regex = '^rss/$',
        view = cache_page(GuideFeed(), FEED_CACHE_TIME),
        kwargs = {},
        name = 'guide_list_feed',
    ),
    url(
        regex = '^(?P<slug>[-\w]+)/$',
        view = cache_page(GuideDetail.as_view(), STANDARD_CACHE_TIME),
        kwargs = {},
        name = 'guide_detail',
    ),
)
