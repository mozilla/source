from django.contrib import admin

from .models import Code, CodeLink
from source.base.widgets import AdminImageMixin

class CodeLinkInline(admin.StackedInline):
    model = CodeLink
    extra = 1
    fieldsets = (
        ('', {'fields': (('name', 'url'),)}),
    )
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        # More usable width in admin form field for names
        field = super(CodeLinkInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'name':
            field.widget.attrs['style'] = 'width: 30em;'
        return field

class CodeAdmin(AdminImageMixin, admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('people', 'organizations',)
    list_filter = ('is_live', 'is_active',)
    search_fields = ('name', 'description',)
    fieldsets = (
        ('', {'fields': (('name', 'slug'), ('is_live', 'is_active', 'seeking_contributors'), 'url', 'tags', 'technology_tags', 'concept_tags', 'screenshot', 'description', 'summary',)}),
        ('Related objects', {'fields': ('people', 'organizations',)}),
    )
    inlines = [CodeLinkInline,]
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        # More usable heights and widths in admin form fields
        field = super(CodeAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['url','tags','technology_tags','concept_tags']:
            field.widget.attrs['style'] = 'width: 45em;'
        if db_field.name in ['name','slug']:
            field.widget.attrs['style'] = 'width: 30em;'
        if db_field.name == 'summary':
            field.widget.attrs['style'] = 'height: 4.5em;'
        return field

admin.site.register(Code, CodeAdmin)
