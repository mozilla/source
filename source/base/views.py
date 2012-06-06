from django.views.generic import ListView

from source.articles.models import Article


ARTICLE_TYPE_MAP = {
    'community': 'Community',
    'project': 'Projects',
    'how-to': 'How-Tos',
    'event': 'Events',
    'this-week': 'This Week in News Code',
}


class HomepageView(ListView):
    model = Article
