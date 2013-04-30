from django.core.management.base import BaseCommand
from source.articles.models import Article, Category

class Command(BaseCommand):
    help = "One-time command to migrate articles to new FK relationship with Category model"
    def handle(self, *args, **options):
        article_set = Article.objects.all()
        category_set = list(Category.objects.all())
        failed_articles = []
        for article in article_set:
            print "Migrating " + article.title
            try:
                print "  looking for " + article.article_type + "..."
                category = Category.objects.get(slug=article.article_type)
                article.category = category
                article.save()
                print "  found a match!"
            except:
                print "  category not found :("
                failed_articles.append(article.title)

        print "Failed to match: " + str(failed_articles)