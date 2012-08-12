from haystack import indexes
from .models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    title = indexes.CharField(model_attr='title', boost=1.2)
    text = indexes.CharField(document=True, use_template=True)
    pubdate = indexes.DateTimeField(model_attr='pubdate')

    def get_model(self):
        return Article

    def get_updated_field(self):
        return 'modified'
        
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().live_objects.all()
