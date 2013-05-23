from django.db.models import Q
from django.http import Http404

from .models import TechnologyTag, ConceptTag
from taggit.models import Tag

def filter_queryset_by_tags(queryset, tag_slugs, tags=[]):
    '''
    This takes a queryset and a set of tag slugs, and:
    - does the proper checks to make sure that each tag actually exists
    - filters the provided queryset based on those tags
    - returns that queryset along with a list of matched tag model instances
    for use in page context
    
    Because we need to match against multiple tag models, we have to do
    some loops I wish we didn't have to do. This is why we cache.
    
    The `tag_slugs` argument should be a string captured by a url param,
    with individual tags separated by a "+" character. The `tags` argument
    should very likely be an empty list, which will end up holding a set
    of model instances for the tags from `tag_slugs`.
    
    This assumes the model for the queryset includes `tags`, `technology_tags`
    and `concept_tags` fields.
    
    The `get_validated_tag_list` and `get_tag_filtered_queryset` functions
    are split into separate pieces so they can be used independently. By the
    feeds framework, for example.
    
    The original `tags` field still exists, and mirrors the contents
    of the split tagfields. This provides some utility for building queries,
    and has the side effect of making sure django-taggit still works.
    '''

    _tag_slug_list = tag_slugs.split('+')
    tags = get_validated_tag_list(_tag_slug_list, tags)
    queryset = get_tag_filtered_queryset(queryset, _tag_slug_list)

    # make sure we actually have matches for this intersection of tags
    if not queryset:
        raise Http404
    
    return queryset, tags


def get_validated_tag_list(tag_slug_list, tags=[]):
    _slugs_checked = []
    for slug in tag_slug_list:
        for model in [TechnologyTag, ConceptTag, Tag]:
            try:
                # see if we have a matching tag
                found_tag = model.objects.get(slug=slug)
                # add it to list for page context
                tags.append(found_tag)
                # remember that we've checked it
                _slugs_checked.append(slug)
                break
            except:
                pass

    # make sure that we found everything we checked for
    if _slugs_checked != tag_slug_list:
        raise Http404
    
    return tags


def get_tag_filtered_queryset(queryset, tag_slug_list=[]):
    for tag_slug in tag_slug_list:
        # Because tags are mirrored in primary tag model, just hit that
        queryset = queryset.filter(tags__slug=tag_slug)

        # Alternatively: Remove original `tags` query, only use split tagfields
        # queryset = queryset.filter(Q(technology_tags__slug=tag_slug) | Q(concept_tags__slug=tag_slug))

        # A record might match multiple tags, but we only want it once
        queryset = queryset.distinct()

    return queryset
