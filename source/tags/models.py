from django.db import models

from taggit.models import GenericTaggedItemBase, TagBase


class TechnologyTag(TagBase):
    pass
    
class TechnologyTaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(TechnologyTag, related_name="%(app_label)s_%(class)s_items")
    
class ConceptTag(TagBase):
    pass

class ConceptTaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(ConceptTag, related_name="%(app_label)s_%(class)s_items")