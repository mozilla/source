from django.conf.urls.defaults import *

from .feeds import ArticleFeed
from source.articles.views import ArticleList, CATEGORY_MAP, SECTION_MAP

article_category_options = "|".join(CATEGORY_MAP.keys())

urlpatterns = patterns('',
    url(
        regex = '^$',
        view = ArticleList.as_view(),
        kwargs = {},
        name = 'homepage',
    ),
    url(
        regex = '^rss/$',
        view = ArticleFeed(),
        kwargs = {},
        name = 'homepage_feed',
    ),
    url(
        regex = '^(?P<section>articles|community)/$',
        view = ArticleList.as_view(),
        kwargs = {},
        name = 'article_list_by_section',
    ),
    url(
        regex = '^(?P<section>articles|community)/rss/$',
        view = ArticleFeed(),
        kwargs = {},
        name = 'article_list_by_section_feed',
    ),
    url(
        regex = '^category/(?P<category>%s)/$' % article_category_options,
        view = ArticleList.as_view(),
        kwargs = {},
        name = 'article_list_by_category',
    ),
    url(
        regex = '^category/(?P<category>%s)/rss/$' % article_category_options,
        view = ArticleFeed(),
        kwargs = {},
        name = 'article_list_by_category_feed',
    ),
    (r'^articles/', include('source.articles.urls')),
    (r'^code/', include('source.code.urls')),
    (r'^people/', include('source.people.urls.people')),
    (r'^organizations/', include('source.people.urls.organizations')),
)
