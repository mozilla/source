from django.contrib import admin

from .models import Person, PersonLink, Organization, OrganizationLink
from source.base.widgets import AdminImageMixin

class PersonLinkInline(admin.StackedInline):
    model = PersonLink
    extra = 1
    fieldsets = (
        ('', {'fields': (('name', 'url'),)}),
    )
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(PersonLinkInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'name':
            field.widget.attrs['style'] = 'width: 30em;'
        return field

class PersonAdmin(admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    list_filter = ('is_live', 'show_in_lists',)
    filter_horizontal = ('organizations',)
    search_fields = ('first_name', 'last_name', 'description',)
    fieldsets = (
        ('', {'fields': (('first_name', 'last_name', 'slug'), ('is_live', 'show_in_lists'), ('email', 'twitter_username', 'github_username',), 'description',)}),
        ('Related objects', {'fields': ('organizations',)}),
    )
    inlines = [PersonLinkInline,]

class OrganizationLinkInline(admin.StackedInline):
    model = OrganizationLink
    extra = 1
    fieldsets = (
        ('', {'fields': (('name', 'url'),)}),
    )
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(OrganizationLinkInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'name':
            field.widget.attrs['style'] = 'width: 30em;'
        return field

class OrganizationAdmin(AdminImageMixin, admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_live',)
    search_fields = ('name', 'description',)
    fieldsets = (
        ('', {'fields': (('name', 'slug'), ('is_live', 'show_in_lists'), 'twitter_username', 'github_username', 'homepage', 'logo', 'description',)}),
        ('Location', {'fields': ('address', ('city', 'state',), 'country',)}),
    )
    inlines = [OrganizationLinkInline,]

admin.site.register(Person, PersonAdmin)
admin.site.register(Organization, OrganizationAdmin)
