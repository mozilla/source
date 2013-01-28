from django.contrib import admin

from .models import Article, ArticleBlock
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
        return field

class ArticleAdmin(AdminImageMixin, admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('authors', 'people', 'organizations', 'code',)
    list_filter = ('is_live', 'article_type',)
    search_fields = ('title', 'body', 'summary',)
    date_hierarchy = 'pubdate'
    fieldsets = (
        ('', {'fields': (('title', 'slug'), 'subhead', ('pubdate', 'is_live'),)}),
        ('Article relationships', {'fields': ('authors', 'people', 'organizations', 'code',)}),
        ('Article body', {'fields': ('article_type', 'tags', 'image', 'image_caption', 'image_credit', 'summary', 'body', 'disable_auto_linebreaks')}),
    )
    inlines = [ArticleBlockInline,]
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        # More usable heights and widths in admin form fields
        field = super(ArticleAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['subhead','tags']:
            field.widget.attrs['style'] = 'width: 45em;'
        if db_field.name in ['title','slug']:
            field.widget.attrs['style'] = 'width: 30em;'
        if db_field.name == 'image_caption':
            field.widget.attrs['style'] = 'height: 5em;'
        return field

admin.site.register(Article, ArticleAdmin)
