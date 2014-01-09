from django.contrib import admin

from .models import Job

class JobAdmin(admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('tweeted_at',)
    list_filter = ('is_live', 'organization',)
    list_display = ('name', 'organization', 'will_show_on_site', 'listing_start_date', 'listing_end_date')
    search_fields = ('name', 'organization__name',)
    fieldsets = (
        ('', {'fields': (('name', 'slug'), 'organization', 'url', 'tweeted_at', 'listing_start_date', 'listing_end_date', 'is_live',)}),
    )

admin.site.register(Job, JobAdmin)
