from django.views.generic import ListView

from source.articles.models import Article


class HomepageView(ListView):
    model = Article
