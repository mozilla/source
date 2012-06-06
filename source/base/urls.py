from django.conf.urls.defaults import *

from .views import HomepageView
from source.articles.views import ArticleList


urlpatterns = patterns('',
    url(
        regex = '^$',
        view = HomepageView.as_view(),
        kwargs = {},
        name = 'homepage',
    ),
    url(
        regex = '^(?P<section>projects|community)/$',
        view = ArticleList.as_view(),
        kwargs = {},
        name = 'article_list_by_section',
    ),
    (r'^articles/', include('source.articles.urls')),
    (r'^code/', include('source.code.urls')),
    (r'^people/', include('source.people.urls.people')),
    (r'^organizations/', include('source.people.urls.organizations')),
)
