from django.conf import settings
from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page

from .views import JobList, JobUpdate
from source.base.feeds import JobFeed

STANDARD_CACHE_TIME = getattr(settings, 'CACHE_MIDDLEWARE_SECONDS', 60*15)
FEED_CACHE_TIME = getattr(settings, 'FEED_CACHE_SECONDS', 60*15)

urlpatterns = patterns('',
    url(
        regex = '^$',
        view = cache_page(JobList.as_view(), STANDARD_CACHE_TIME),
        kwargs = {},
        name = 'job_list',
    ),
    url(
        regex = '^rss/$',
        view = cache_page(JobFeed(), FEED_CACHE_TIME),
        kwargs = {},
        name = 'job_list_feed',
    ),
    url(
        regex = '^json/$',
        view = cache_page(JobList.as_view(), FEED_CACHE_TIME),
        kwargs = {'render_json': True},
        name = 'job_list_feed_json',
    ),
    url(
        regex = '^update/$',
        view = JobUpdate.as_view(),
        kwargs = {},
        name = 'job_update',
    ),
)
