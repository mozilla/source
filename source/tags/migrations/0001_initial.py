# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TechnologyTag'
        db.create_table('tags_technologytag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('tags', ['TechnologyTag'])

        # Adding model 'TechnologyTaggedItem'
        db.create_table('tags_technologytaggeditem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tags_technologytaggeditem_tagged_items', to=orm['contenttypes.ContentType'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tags_technologytaggeditem_techtag_items', to=orm['tags.TechnologyTag'])),
        ))
        db.send_create_signal('tags', ['TechnologyTaggedItem'])

        # Adding model 'ConceptTag'
        db.create_table('tags_concepttag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('tags', ['ConceptTag'])

        # Adding model 'ConceptTaggedItem'
        db.create_table('tags_concepttaggeditem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tags_concepttaggeditem_tagged_items', to=orm['contenttypes.ContentType'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tags_concepttaggeditem_concepttag_items', to=orm['tags.ConceptTag'])),
        ))
        db.send_create_signal('tags', ['ConceptTaggedItem'])


    def backwards(self, orm):
        # Deleting model 'TechnologyTag'
        db.delete_table('tags_technologytag')

        # Deleting model 'TechnologyTaggedItem'
        db.delete_table('tags_technologytaggeditem')

        # Deleting model 'ConceptTag'
        db.delete_table('tags_concepttag')

        # Deleting model 'ConceptTaggedItem'
        db.delete_table('tags_concepttaggeditem')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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

    complete_apps = ['tags']