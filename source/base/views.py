from django.views.generic import ListView

from haystack.views import SearchView
from source.articles.views import ArticleList
from source.code.models import Code


class HomepageView(ArticleList):
    '''
    Gets standard list of articles from articles.views.ArticleList, then adds
    recent code additions to context for homepage aside block.
    '''
    def get_homepage_aside_context(self, context):
        code_list = Code.live_objects.order_by('-created').prefetch_related('people', 'organizations')
        
        # wrap in try/except in case code_list is empty
        try:
            code_list = code_list[:12]
        except:
            pass
        
        context.update({
            'homepage_code_list': code_list,
        })
        
        return ''
        
    
    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        self.get_standard_context(context)
        self.get_homepage_aside_context(context)
        
        return context

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
    