from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic.simple import redirect_to

from .views import CodeList, CodeDetail
from source.base.feeds import CodeFeed


urlpatterns = patterns('',
    url(
        regex = '^$',
        view = CodeList.as_view(),
        kwargs = {},
        name = 'code_list',
    ),
    url(
        regex = '^rss/$',
        view = cache_page(CodeFeed(), 60*15),
        kwargs = {},
        name = 'code_list_feed',
    ),
    url(
        regex = '^tags/(?P<tag_slug>[-\w]+)/$',
        view = CodeList.as_view(),
        kwargs = {},
        name = 'code_list_by_tag',
    ),
    url(
        regex = '^tags/(?P<tag_slug>[-\w]+)/rss/$',
        view = cache_page(CodeFeed(), 60*15),
        kwargs = {},
        name = 'code_list_by_tag_feed',
    ),
    url(
        regex = '^tags/$',
        view = redirect_to,
        kwargs  = {'url': '/code/'},
        name = 'code_list_tags',
    ),
    url(
        regex = '^(?P<slug>[-\w]+)/$',
        view = CodeDetail.as_view(),
        kwargs = {},
        name = 'code_detail',
    ),
)
