from django.contrib import admin

from .models import Job

class JobAdmin(admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_live', 'organization',)
    list_display = ('name', 'organization', 'will_show_on_site', 'listing_start_date', 'listing_end_date', 'tweeted_at')
    search_fields = ('name', 'organization__name',)
    fieldsets = (
        ('', {'fields': (('name', 'slug'), 'description', 'organization', 'location', 'url', 'contact_name', 'email', 'tweeted_at', 'listing_start_date', 'listing_end_date', 'is_live',)}),
    )
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        # More usable heights and widths in admin form fields
        field = super(JobAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'description':
            field.widget.attrs['style'] = 'height: 3em;'
        return field
    

admin.site.register(Job, JobAdmin)
