from django.conf import settings
from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page

from .views import JobList
#from source.base.feeds import JobFeed

STANDARD_CACHE_TIME = getattr(settings, 'CACHE_MIDDLEWARE_SECONDS', 60*15)
FEED_CACHE_TIME = getattr(settings, 'FEED_CACHE_SECONDS', 60*15)

urlpatterns = patterns('',
    url(
        regex = '^$',
        view = cache_page(JobList.as_view(), STANDARD_CACHE_TIME),
        kwargs = {},
        name = 'job_list',
    ),
)
