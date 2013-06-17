from django.contrib import admin

from .models import Job

class JobAdmin(admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_live', 'organization',)
    search_fields = ('name', 'description',)
    fieldsets = (
        ('', {'fields': (('name', 'slug', 'is_live'), 'organization', ('listing_start_date', 'listing_end_date'),)}),
        ('Job Details', {'fields': ('description', 'summary', 'requirements', 'salary', 'location', 'job_start_date', 'url')}),
    )

admin.site.register(Job, JobAdmin)
