from django.contrib import admin

from .models import Person, PersonLink, Organization, OrganizationLink

class PersonLinkInline(admin.StackedInline):
    model = PersonLink
    extra = 1

class PersonAdmin(admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    list_filter = ('is_live', 'show_in_lists',)
    filter_horizontal = ('organizations',)
    search_fields = ('first_name', 'last_name', 'description',)
    inlines = [PersonLinkInline,]

class OrganizationLinkInline(admin.StackedInline):
    model = OrganizationLink
    extra = 1

class OrganizationAdmin(admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_live',)
    search_fields = ('name', 'description',)
    inlines = [OrganizationLinkInline,]

admin.site.register(Person, PersonAdmin)
admin.site.register(Organization, OrganizationAdmin)