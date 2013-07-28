from django.conf import settings
from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page

from source.people.views import PersonList, PersonDetail, PersonUpdate, PersonSearchJson

STANDARD_CACHE_TIME = getattr(settings, 'CACHE_MIDDLEWARE_SECONDS', 60*15)

urlpatterns = patterns('',
    url(
        regex = '^$',
        view = cache_page(PersonList.as_view(), STANDARD_CACHE_TIME),
        kwargs = {},
        name = 'person_list',
    ),
    url(
        regex = '^update/$',
        view = PersonUpdate.as_view(),
        kwargs = {},
        name = 'person_update',
    ),
    url(
        regex   = '^json/$',
        view    = PersonSearchJson.as_view(),
        kwargs  = {},
        name    = 'person_search_json',
    ),
    url(
        regex = '^(?P<slug>[-\w]+)/$',
        view = cache_page(PersonDetail.as_view(), STANDARD_CACHE_TIME),
        kwargs = {},
        name = 'person_detail',
    ),
)
