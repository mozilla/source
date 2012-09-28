from django.views.generic import ListView

from haystack.views import SearchView


class HomepageView(ListView):
    '''
    For now, this request runs through articles.views.ArticleList
    '''
    pass

class SourceSearchView(SearchView):
    def extra_context(self):
        return {
            'hide_topbar_search': True
        }
    