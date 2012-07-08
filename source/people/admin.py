from django.contrib import admin

from .models import Person, PersonLink, Organization, OrganizationLink

class PersonLinkInline(admin.StackedInline):
    model = PersonLink
    extra = 1
    fieldsets = (
        ('', {'fields': (('name', 'url'),)}),
    )

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

class OrganizationAdmin(admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_live',)
    search_fields = ('name', 'description',)
    fieldsets = (
        ('', {'fields': (('name', 'slug'), 'is_live', 'twitter_username', 'github_username', 'description',)}),
        ('Location', {'fields': ('address', ('city', 'state',), 'country',)}),
    )
    inlines = [OrganizationLinkInline,]

admin.site.register(Person, PersonAdmin)
admin.site.register(Organization, OrganizationAdmin)