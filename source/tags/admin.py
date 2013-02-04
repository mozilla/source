from django.contrib import admin

from .models import TechnologyTag, TechnologyTaggedItem, ConceptTag, ConceptTaggedItem


class TechnologyTaggedItemInline(admin.StackedInline):
    model = TechnologyTaggedItem

class TechnologyTagAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [
        TechnologyTaggedItemInline
    ]

class ConceptTaggedItemInline(admin.StackedInline):
    model = ConceptTaggedItem

class ConceptTagAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [
        ConceptTaggedItemInline
    ]

admin.site.register(TechnologyTag, TechnologyTagAdmin)
admin.site.register(ConceptTag, ConceptTagAdmin)
