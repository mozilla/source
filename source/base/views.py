from django.views.generic import ListView

from haystack.views import SearchView
from source.articles.models import Article
from source.articles.views import ArticleList
from source.code.models import Code
from source.people.models import Organization, Person


class HomepageView(ArticleList):
    '''
    Gets standard list of articles from articles.views.ArticleList, then adds
    recent code additions to context for homepage aside block.
    '''
    def get_homepage_aside_context(self, context):
        code_list = Code.live_objects.order_by('-created').prefetch_related('people', 'organizations')
        
        # wrap in try/except in case code_list is empty
        try:
            code_list = code_list[:15]
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
    def get_results(self):
        '''
        Limit primary search results to Article and Code matches.
        Template gets Person and Organization matches separately,
        via `get_secondary_results`.
        '''
        results = self.form.search().models(Article, Code)
        return results
    
    def get_person_results(self):
        '''
        Get Person matches for separate handling on template.
        '''
        person_results = self.form.search().models(Person)
        return person_results

    def get_organization_results(self):
        '''
        Get Organization matches for separate handling on template.
        '''
        organization_results = self.form.search().models(Organization)
        return organization_results
    
    def extra_context(self):
        page_context = {
            'content_type_map': {
                'article': 'Articles',
                'code': 'Code',
                'organization': 'Organizations',
                'person': 'People',
            }
        }
        
        if self.query:
            page_context.update({
                'person_results': self.get_person_results(),
                'organization_results': self.get_organization_results()
            })
        
        return page_context
    