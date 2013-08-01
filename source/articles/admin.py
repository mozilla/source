from django.contrib import admin

from .models import Article, ArticleBlock, Section, Category
from source.base.widgets import AdminImageMixin

class ArticleBlockInline(AdminImageMixin, admin.StackedInline):
    model = ArticleBlock
    extra = 1
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('', {'fields': ('order', ('title', 'slug'), 'body', ('image', 'image_presentation'), 'image_caption', 'image_credit',)}),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        # More usable height in admin form fields for captions
        field = super(ArticleBlockInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'image_caption':
            field.widget.attrs['style'] = 'height: 5em;'
        if db_field.name == 'image_credit':
            field.widget.attrs['style'] = 'width: 45em;'
        return field

class ArticleAdmin(AdminImageMixin, admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('authors', 'people', 'organizations', 'code',)
    list_filter = ('is_live', 'category',)
    list_display = ('title', 'pubdate', 'category', 'is_live')
    search_fields = ('title', 'body', 'summary',)
    date_hierarchy = 'pubdate'
    fieldsets = (
        ('', {'fields': (('pubdate', 'is_live', 'show_in_lists', 'allow_comments'), ('title', 'slug'), 'subhead', ('category', 'tags'), 'technology_tags', 'concept_tags',)}),
        ('Article relationships', {'fields': ('authors', 'people', 'organizations', 'code',)}),
        ('Article body', {'fields': ('image', 'image_caption', 'image_credit', 'summary', 'body', 'disable_auto_linebreaks')}),
    )
    inlines = [ArticleBlockInline,]
    readonly_fields = ('tags',)

    def save_model(self, request, obj, form, change):
        '''
        Mirror split tagfield contents in primary `tags` model.
        See source.tags.models for further details.
        '''
        technology_tags_list = form.cleaned_data['technology_tags']
        concept_tags_list = form.cleaned_data['concept_tags']
        merged_tags = technology_tags_list + concept_tags_list
        if merged_tags:
            form.cleaned_data['tags'] = merged_tags

        super(ArticleAdmin, self).save_model(request, obj, form, change)
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        # More usable heights and widths in admin form fields
        field = super(ArticleAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['subhead','tags','technology_tags','concept_tags','image_credit']:
            field.widget.attrs['style'] = 'width: 45em;'
        if db_field.name in ['title','slug']:
            field.widget.attrs['style'] = 'width: 30em;'
        if db_field.name == 'image_caption':
            field.widget.attrs['style'] = 'height: 5em;'
        return field

class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1
    prepopulated_fields = {'slug': ('name',)}

class SectionAdmin(AdminImageMixin, admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CategoryInline,]

admin.site.register(Article, ArticleAdmin)
admin.site.register(Section, SectionAdmin)
