from django.conf import settings
from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page

from .views import ContributorCount

FEED_CACHE_TIME = getattr(settings, 'FEED_CACHE_SECONDS', 60*15)

urlpatterns = patterns('',
    url(
        regex = '^contributor-count/$',
        view = cache_page(ContributorCount.as_view(), FEED_CACHE_TIME),
        kwargs = {},
        name = 'api_v1_contributor_count',
    ),
)
