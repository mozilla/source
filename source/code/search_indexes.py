from haystack import indexes
from .models import Code


class CodeIndex(indexes.SearchIndex, indexes.Indexable):
    name = indexes.CharField(model_attr='name', boost=1.2)
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Code

    def get_updated_field(self):
        return 'modified'
        
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().live_objects.all()
