'''
We currently use tags for filtering on these content models:

- Article
- Code

Originally there was but one `tags` field on each model, and it was good.
But lo and verily, @slifty asked for split tagfields, to differentiate
between technologies and concepts. And this seemed beautiful to our eyes.

It also seemed so very simple to implement. But as I have discovered, 
django-taggit is in no way designed to accommodate multiple TaggableManagers
on a given model. This app gives us a way to work around this limitation.
But beautiful it is not.

To implement split tagfields, a model should keep its original `tags` field,
and then add `technology_tags` and `concept_tags` fields as TaggableManagers
with `through` properties pointing at this app's FooTaggedItem fields.

Additionally, that model's admin class should set the original `tags` field
to readonly, and implement a `save_model` that automatically populates `tags`
with a concatenated list of `technology_tags` and `concept_tags`.

Yes, this denormalizes things somewhat. But it enables much simpler code for
displaying lists of tags, and because of the way django-taggit operates,
having *something* in that `tags` field turns out to be critical for proper
filtering of querysets, *even against the two split tagfields*. You would
think that a filter like so ...

    queryset.filter(
        Q(tags__slug=tag_slug) | 
        Q(technology_tags__slug=tag_slug) | 
        Q(concept_tags__slug=tag_slug)
    )

... would work just fine, but because of something deep down inside
django-taggit, this filter will *not* return an object that has a null
value in `tags`. Even if you entirely remove the `tags` field from
the filter, this problem still exists. Even if you remove the `tags` field
from the model itself, the problem still exists; it just migrates to
`technology_tags` (or whichever TaggableManager appears first in the model
code.)

Patches against django-taggit have thus far failed to solve the problem. And
"problem" might not be the right way to put it; that app was never designed
to support a use case with multiple kinds of tags. Because the denormalized
version that keeps `tags` around *does* offer some benefits, however, this is
where we stand for now.

TODO: Figure out that filter bug wtf
'''
from django.db import models

from taggit.models import GenericTaggedItemBase, TagBase


class TechnologyTag(TagBase):
    pass
    
class TechnologyTaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(TechnologyTag, related_name="%(app_label)s_%(class)s_techtag_items")
    
class ConceptTag(TagBase):
    pass

class ConceptTaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(ConceptTag, related_name="%(app_label)s_%(class)s_concepttag_items")
    