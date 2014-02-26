from django.contrib import admin

from .models import Guide, GuideArticle
from source.base.widgets import AdminImageMixin

class GuideArticleInline(admin.StackedInline):
    model = GuideArticle
    extra = 1
    raw_id_fields = ('article',)
    fieldsets = (
        ('', {'fields': ('article', 'order', 'article_notes')}),
    )
    
class GuideAdmin(AdminImageMixin, admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_live', 'show_in_lists',)
    search_fields = ('title', 'summary', 'description',)
    fieldsets = (
        ('', {'fields': (('pubdate', 'is_live', 'show_in_lists'), ('title', 'slug'), 'description', 'summary')}),
        ('', {'fields': ('cover_color', 'image')}),
    )
    inlines = [GuideArticleInline,]
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        # More usable heights and widths in admin form fields
        field = super(GuideAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['title','slug']:
            field.widget.attrs['style'] = 'width: 30em;'
        if db_field.name == 'summary':
            field.widget.attrs['style'] = 'height: 4.5em;'
        return field

admin.site.register(Guide, GuideAdmin)
