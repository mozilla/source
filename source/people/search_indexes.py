from haystack import indexes
from .models import Person, Organization


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    name = indexes.CharField(model_attr='name', boost=1.2)
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Person

    def get_updated_field(self):
        return 'modified'
        
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().live_objects.all()


class OrganizationIndex(indexes.SearchIndex, indexes.Indexable):
    name = indexes.CharField(model_attr='name', boost=1.2)
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Organization

    def get_updated_field(self):
        return 'modified'

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().live_objects.all()
