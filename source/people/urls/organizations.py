from django.conf import settings
from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from source.people.views import OrganizationList, OrganizationDetail, OrganizationManage

STANDARD_CACHE_TIME = getattr(settings, 'CACHE_MIDDLEWARE_SECONDS', 60*15)

urlpatterns = patterns('',
    url(
        regex = '^$',
        view = cache_page(OrganizationList.as_view(), STANDARD_CACHE_TIME),
        kwargs = {},
        name = 'organization_list',
    ),
    url(
        regex = '^manage/$',
        view = OrganizationManage.as_view(),
        kwargs = {},
        name = 'organization_manage',
    ),
    url(
        regex = '^(?P<slug>[-\w]+)/$',
        view = cache_page(OrganizationDetail.as_view(), STANDARD_CACHE_TIME),
        kwargs = {},
        name = 'organization_detail',
    ),
)
