from django.http import Http404
from django.test import TestCase

from source.code.models import Code
from source.tags.models import TechnologyTag, ConceptTag
from source.tags.utils import (get_validated_tag_list,
    get_tag_filtered_queryset, filter_queryset_by_tags)


class BaseTestCase(TestCase):
    def assertQuerysetEqual(self, qs1, qs2):
        pk = lambda o: o.pk
        return self.assertEqual(
            list(sorted(qs1, key=pk)),
            list(sorted(qs2, key=pk))
        )
        
class TestCodeTagAdd(BaseTestCase):
    code_model = Code
    tech_tag_model = TechnologyTag
    concept_tag_model = ConceptTag
    
    def setUp(self):
        self.tech_tag = self.tech_tag_model.objects.create(name="javascript", slug="javascript")
        self.concept_tag = self.concept_tag_model.objects.create(name="mapping", slug="mapping")
        self.code_one = self.code_model.objects.create(name="supermaps", slug="supermaps")
        self.code_two = self.code_model.objects.create(name="justmaps", slug="justmaps")
        self.code_three = self.code_model.objects.create(name="justjs", slug="justjs")
        
    def test_code_entries(self):
        self.assertEqual(self.code_one.title, "supermaps")
        self.assertEqual(self.code_two.title, "justmaps")
        self.assertEqual(self.code_three.title, "justjs")
        
    def test_add_tags(self):
        # make sure code_one has two empty tagfields
        self.assertEqual(list(self.code_one.technology_tags.all()), [])
        self.assertEqual(list(self.code_one.concept_tags.all()), [])
        # add one tag of each kind
        self.code_one.technology_tags.add("javascript")
        self.code_one.concept_tags.add("mapping")
        # make sure code_one has the right tags in each tagfield
        self.assertEqual(list(self.code_one.technology_tags.all()), [self.tech_tag])
        self.assertEqual(list(self.code_one.concept_tags.all()), [self.concept_tag])

        # make sure code_two has two empty tagfields
        self.assertEqual(list(self.code_two.technology_tags.all()), [])
        self.assertEqual(list(self.code_two.concept_tags.all()), [])
        # add just one concept tag
        self.code_two.concept_tags.add("mapping")
        # make sure code_two has the right tags in each tagfield
        self.assertEqual(list(self.code_two.technology_tags.all()), [])
        self.assertEqual(list(self.code_two.concept_tags.all()), [self.concept_tag])

        # make sure code_three has two empty tagfields
        self.assertEqual(list(self.code_three.technology_tags.all()), [])
        self.assertEqual(list(self.code_three.concept_tags.all()), [])
        # add just one technology tag
        self.code_three.technology_tags.add("javascript")
        # make sure code_three has the right tags in each tagfield
        self.assertEqual(list(self.code_three.technology_tags.all()), [self.tech_tag])
        self.assertEqual(list(self.code_three.concept_tags.all()), [])

class TestCodeTagQueries(BaseTestCase):
    code_model = Code
    tech_tag_model = TechnologyTag
    concept_tag_model = ConceptTag

    def setUp(self):
        self.tech_tag = self.tech_tag_model.objects.create(name="javascript", slug="javascript")
        self.concept_tag = self.concept_tag_model.objects.create(name="mapping", slug="mapping")
        # first code entry gets one tag of each kind
        self.code_one = self.code_model.objects.create(name="supermaps", slug="supermaps")
        self.code_one.technology_tags.add("javascript")
        self.code_one.concept_tags.add("mapping")
        # second code entry gets just one concept tag
        self.code_two = self.code_model.objects.create(name="justmaps", slug="justmaps")
        self.code_two.concept_tags.add("mapping")
        # third code entry gets just one tech tag
        self.code_three = self.code_model.objects.create(name="justjs", slug="justjs")
        self.code_three.technology_tags.add("javascript")
        # this is not ideal, but because of django-taggit internals,
        # we can't filter querysets based on tags unless we compile all
        # technology_tags and concept_tags into a common `tags` list too
        self.code_one.tags.add("javascript","mapping")
        self.code_two.tags.add("mapping")
        self.code_three.tags.add("javascript")
        
        
    def test_tags_added_properly(self):
        self.assertEqual(list(self.code_one.technology_tags.all()), [self.tech_tag])
        self.assertEqual(list(self.code_one.concept_tags.all()), [self.concept_tag])
        self.assertEqual(list(self.code_two.concept_tags.all()), [self.concept_tag])
        self.assertEqual(list(self.code_three.technology_tags.all()), [self.tech_tag])

    def test_get_validated_tag_list(self):
        tag_slug_list_one = ["javascript", "mapping"]
        tags_one = get_validated_tag_list(tag_slug_list_one)
        self.assertEqual(tags_one, [self.tech_tag, self.concept_tag])
        
        tag_slug_list_two = ["javascript", "mapping", "this_tag_does_not_exist"]
        self.assertRaises(Http404, lambda: get_validated_tag_list(tag_slug_list_two))
        
    def test_get_tag_filtered_queryset(self):
        code_objects = self.code_model.objects.all()

        tag_slug_list_one = ["javascript", "mapping"]
        queryset_one = get_tag_filtered_queryset(code_objects, tag_slug_list_one)
        self.assertQuerysetEqual(queryset_one, [self.code_one])

        tag_slug_list_two = ["mapping"]
        queryset_two = get_tag_filtered_queryset(code_objects, tag_slug_list_two)
        self.assertQuerysetEqual(queryset_two, [self.code_one, self.code_two])

        tag_slug_list_three = ["javascript"]
        queryset_three = get_tag_filtered_queryset(code_objects, tag_slug_list_three)
        self.assertQuerysetEqual(queryset_three, [self.code_one, self.code_three])
        
    def test_filter_queryset_by_tags(self):
        code_objects = self.code_model.objects.all()

        tag_slugs_one = "javascript+mapping"
        queryset_one, tags_one = filter_queryset_by_tags(code_objects, tag_slugs_one, tags=[])
        self.assertQuerysetEqual(queryset_one, [self.code_one])
        self.assertEqual(tags_one, [self.tech_tag, self.concept_tag])
        
        tag_slugs_two = "mapping"
        queryset_two, tags_two = filter_queryset_by_tags(code_objects, tag_slugs_two, tags=[])
        self.assertQuerysetEqual(queryset_two, [self.code_one, self.code_two])
        self.assertEqual(tags_two, [self.concept_tag])
        
        tag_slugs_three = "javascript"
        queryset_three, tags_three = filter_queryset_by_tags(code_objects, tag_slugs_three, tags=[])
        self.assertQuerysetEqual(queryset_three, [self.code_one, self.code_three])
        self.assertEqual(tags_three, [self.tech_tag])

        tag_slugs_four = "javascript+this_tag_does_not_exist"
        self.assertRaises(Http404, lambda: filter_queryset_by_tags(
            code_objects, tag_slugs_four, tags=[])
        )
        