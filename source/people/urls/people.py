from django.conf.urls.defaults import *

from source.people.views import PersonList, PersonDetail


urlpatterns = patterns('',
    url(
        regex = '^$',
        view = PersonList.as_view(),
        kwargs = {},
        name = 'person_list',
    ),
    url(
        regex = '^(?P<slug>[-\w]+)/$',
        view = PersonDetail.as_view(),
        kwargs = {},
        name = 'person_detail',
    ),
)
