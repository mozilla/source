from django.conf.urls.defaults import *

#from .views import HomepageView
from source.articles.views import ArticleList, CATEGORY_MAP, SECTION_MAP

article_category_options = "|".join(CATEGORY_MAP.keys())
#article_category_options = "|".join(
#    [item for article_types in [SECTION_MAP[s]['article_types'] for s in SECTION_MAP] #for item in article_types]
#)

urlpatterns = patterns('',
    url(
        regex = '^$',
        view = ArticleList.as_view(),
        kwargs = {},
        name = 'homepage',
    ),
    url(
        regex = '^(?P<section>articles|community)/$',
        view = ArticleList.as_view(),
        kwargs = {},
        name = 'article_list_by_section',
    ),
    url(
        regex = '^category/(?P<category>%s)/$' % article_category_options,
        view = ArticleList.as_view(),
        kwargs = {},
        name = 'article_list_by_category',
    ),
    (r'^articles/', include('source.articles.urls')),
    (r'^code/', include('source.code.urls')),
    (r'^people/', include('source.people.urls.people')),
    (r'^organizations/', include('source.people.urls.organizations')),
    (r'^search/', include('haystack.urls')),
)
