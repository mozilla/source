from django.contrib import admin

from .models import Article, ArticleBlock


class ArticleBlockInline(admin.StackedInline):
    model = ArticleBlock
    extra = 1
    prepopulated_fields = {'slug': ('title',)}

class ArticleAdmin(admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('people', 'organizations', 'code',)
    list_filter = ('is_live', 'article_type',)
    search_fields = ('title', 'body', 'summary',)
    date_hierarchy = 'pubdate'
    inlines = [ArticleBlockInline,]

admin.site.register(Article, ArticleAdmin)