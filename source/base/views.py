from django.views.generic import ListView

from haystack.views import SearchView
from source.articles.views import ArticleList

class HomepageView(ArticleList):
    '''
    For now, this request runs through articles.views.ArticleList
    '''
    pass

class SourceSearchView(SearchView):
    def extra_context(self):
        '''
        Add extra context for search results page here.
        '''
        page_context = {
            'content_type_map': {
                'article': 'Articles',
                'code': 'Code',
                'organization': 'Organizations',
                'person': 'People',
            }
        }
        return page_context
    