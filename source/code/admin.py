from django.contrib import admin

from .models import Code, CodeLink

class CodeLinkInline(admin.StackedInline):
    model = CodeLink
    extra = 1

class CodeAdmin(admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('people', 'organizations',)
    list_filter = ('is_live', 'is_active',)
    search_fields = ('name', 'description',)
    inlines = [CodeLinkInline,]

admin.site.register(Code, CodeAdmin)