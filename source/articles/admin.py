from django.contrib import admin

from .models import Article, ArticleBlock


class ArticleBlockInline(admin.StackedInline):
    model = ArticleBlock
    extra = 1
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('', {'fields': ('order', ('title', 'slug'), 'body', ('image', 'image_presentation'),)}),
    )

class ArticleAdmin(admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('authors', 'people', 'organizations', 'code',)
    list_filter = ('is_live', 'article_type',)
    search_fields = ('title', 'body', 'summary',)
    date_hierarchy = 'pubdate'
    fieldsets = (
        ('', {'fields': (('title', 'slug'), 'subhead', ('pubdate', 'is_live'),)}),
        ('Article relationships', {'fields': ('authors', 'people', 'organizations', 'code',)}),
        ('Article body', {'fields': ('article_type', 'tags', 'image', 'summary', 'body',)}),
    )
    inlines = [ArticleBlockInline,]
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(ArticleAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['subhead','tags']:
            field.widget.attrs['style'] = 'width: 45em;'
        if db_field.name in ['title','slug']:
            field.widget.attrs['style'] = 'width: 30em;'
        return field

admin.site.register(Article, ArticleAdmin)