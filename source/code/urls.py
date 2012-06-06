from django.conf.urls.defaults import *
from .views import CodeList, CodeDetail


urlpatterns = patterns('',
    url(
        regex = '^$',
        view = CodeList.as_view(),
        kwargs = {},
        name = 'code_list',
    ),
    url(
        regex = '^(?P<slug>[-\w]+)/$',
        view = CodeDetail.as_view(),
        kwargs = {},
        name = 'code_detail',
    ),
)
