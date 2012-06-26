from django.conf.urls.defaults import *

from source.people.views import OrganizationList, OrganizationDetail


urlpatterns = patterns('',
    url(
        regex = '^$',
        view = OrganizationList.as_view(),
        kwargs = {},
        name = 'organization_list',
    ),
    url(
        regex = '^(?P<slug>[-\w]+)/$',
        view = OrganizationDetail.as_view(),
        kwargs = {},
        name = 'organization_detail',
    ),
)
