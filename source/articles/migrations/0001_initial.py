# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Article'
        db.create_table('articles_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_live', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('show_in_lists', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('allow_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('pubdate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('subhead', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('image_caption', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image_credit', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('summary', self.gf('django.db.models.fields.TextField')()),
            ('article_type', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Category'])),
            ('disable_auto_linebreaks', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('articles', ['Article'])

        # Adding M2M table for field authors on 'Article'
        db.create_table('articles_article_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['articles.article'], null=False)),
            ('person', models.ForeignKey(orm['people.person'], null=False))
        ))
        db.create_unique('articles_article_authors', ['article_id', 'person_id'])

        # Adding M2M table for field people on 'Article'
        db.create_table('articles_article_people', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['articles.article'], null=False)),
            ('person', models.ForeignKey(orm['people.person'], null=False))
        ))
        db.create_unique('articles_article_people', ['article_id', 'person_id'])

        # Adding M2M table for field organizations on 'Article'
        db.create_table('articles_article_organizations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['articles.article'], null=False)),
            ('organization', models.ForeignKey(orm['people.organization'], null=False))
        ))
        db.create_unique('articles_article_organizations', ['article_id', 'organization_id'])

        # Adding M2M table for field code on 'Article'
        db.create_table('articles_article_code', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['articles.article'], null=False)),
            ('code', models.ForeignKey(orm['code.code'], null=False))
        ))
        db.create_unique('articles_article_code', ['article_id', 'code_id'])

        # Adding model 'ArticleBlock'
        db.create_table('articles_articleblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Article'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('image_presentation', self.gf('django.db.models.fields.CharField')(max_length=24, blank=True)),
            ('image_caption', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image_credit', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('articles', ['ArticleBlock'])

        # Adding model 'Section'
        db.create_table('articles_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('gets_promo_items', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('special_template', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('articles', ['Section'])

        # Adding model 'Category'
        db.create_table('articles_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Section'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('articles', ['Category'])


    def backwards(self, orm):
        # Deleting model 'Article'
        db.delete_table('articles_article')

        # Removing M2M table for field authors on 'Article'
        db.delete_table('articles_article_authors')

        # Removing M2M table for field people on 'Article'
        db.delete_table('articles_article_people')

        # Removing M2M table for field organizations on 'Article'
        db.delete_table('articles_article_organizations')

        # Removing M2M table for field code on 'Article'
        db.delete_table('articles_article_code')

        # Deleting model 'ArticleBlock'
        db.delete_table('articles_articleblock')

        # Deleting model 'Section'
        db.delete_table('articles_section')

        # Deleting model 'Category'
        db.delete_table('articles_category')


    models = {
        'articles.article': {
            'Meta': {'ordering': "('-pubdate', 'title')", 'object_name': 'Article'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'article_type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'article_authors'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['people.Person']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Category']"}),
            'code': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['code.Code']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'disable_auto_linebreaks': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image_caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'image_credit': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'is_live': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'organizations': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['people.Organization']", 'null': 'True', 'blank': 'True'}),
            'people': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['people.Person']", 'null': 'True', 'blank': 'True'}),
            'pubdate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'show_in_lists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'subhead': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'articles.articleblock': {
            'Meta': {'ordering': "('article', 'order', 'title')", 'object_name': 'ArticleBlock'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Article']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image_caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'image_credit': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'image_presentation': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'articles.category': {
            'Meta': {'ordering': "('section', 'name')", 'object_name': 'Category'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Section']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'articles.section': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Section'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gets_promo_items': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'special_template': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'code.code': {
            'Meta': {'ordering': "('slug',)", 'object_name': 'Code'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_live': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'organizations': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['people.Organization']", 'null': 'True', 'blank': 'True'}),
            'people': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['people.Person']", 'null': 'True', 'blank': 'True'}),
            'repo_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'repo_forks': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'repo_last_push': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'repo_master_branch': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'repo_watchers': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'screenshot': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'seeking_contributors': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'people.organization': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Organization'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'github_gists_num': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'github_repos_num': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'github_username': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_live': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'logo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'show_in_lists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        },
        'people.person': {
            'Meta': {'ordering': "('last_name', 'first_name')", 'object_name': 'Person'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'github_gists_num': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'github_repos_num': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'github_username': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_live': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'organizations': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['people.Organization']", 'null': 'True', 'blank': 'True'}),
            'show_in_lists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'twitter_bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'twitter_profile_image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        },
        'tags.concepttag': {
            'Meta': {'object_name': 'ConceptTag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'tags.concepttaggeditem': {
            'Meta': {'object_name': 'ConceptTaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tags_concepttaggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tags_concepttaggeditem_concepttag_items'", 'to': "orm['tags.ConceptTag']"})
        },
        'tags.technologytag': {
            'Meta': {'object_name': 'TechnologyTag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'tags.technologytaggeditem': {
            'Meta': {'object_name': 'TechnologyTaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tags_technologytaggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tags_technologytaggeditem_techtag_items'", 'to': "orm['tags.TechnologyTag']"})
        }
    }

    complete_apps = ['articles']