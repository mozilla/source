from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page

from .feeds import ArticleFeed
from .views import SourceSearchView, HomepageView
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory
from source.articles.views import ArticleList, CATEGORY_MAP, SECTION_MAP

article_category_options = "|".join(CATEGORY_MAP.keys())

urlpatterns = patterns('',
    url(
        regex = '^$',
        view = HomepageView.as_view(template_name='homepage.html'),
        kwargs = {},
        name = 'homepage',
    ),
    url(
        regex = '^rss/$',
        view = cache_page(ArticleFeed(), 60*15),
        kwargs = {},
        name = 'homepage_feed',
    ),
    # matching /articles/ here to offer future support for multiple sections
    url(
        regex = '^(?P<section>articles|learning)/$',
        view = ArticleList.as_view(),
        kwargs = {},
        name = 'article_list_by_section',
    ),
    url(
        regex = '^(?P<section>articles|learning)/rss/$',
        view = cache_page(ArticleFeed(), 60*15),
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
        view = cache_page(ArticleFeed(), 60*15),
        kwargs = {},
        name = 'article_list_by_category_feed',
    ),
    url(
        regex = '^search/$',
        view = search_view_factory(view_class=SourceSearchView, form_class=SearchForm, searchqueryset=SearchQuerySet().order_by('django_ct')),
        kwargs = {},
        name = 'haystack_search',
    ),
    (r'^articles/', include('source.articles.urls')),
    (r'^code/', include('source.code.urls')),
    (r'^people/', include('source.people.urls.people')),
    (r'^organizations/', include('source.people.urls.organizations')),
)
