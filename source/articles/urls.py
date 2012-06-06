from django.conf.urls.defaults import *
from .views import ArticleList, ArticleDetail


urlpatterns = patterns('',
    url(
        regex = '^$',
        view = ArticleList.as_view(),
        kwargs = {},
        name = 'article_list',
    ),
    url(
        regex = '^(?P<slug>[-\w]+)/$',
        view = ArticleDetail.as_view(),
        kwargs = {},
        name = 'article_detail',
    ),
)
