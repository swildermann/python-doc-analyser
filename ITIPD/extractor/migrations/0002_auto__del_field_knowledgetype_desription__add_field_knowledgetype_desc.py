# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'KnowledgeType.desription'
        db.delete_column('extractor_knowledgetype', 'desription')

        # Adding field 'KnowledgeType.description'
        db.add_column('extractor_knowledgetype', 'description',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'KnowledgeType.desription'
        db.add_column('extractor_knowledgetype', 'desription',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Deleting field 'KnowledgeType.description'
        db.delete_column('extractor_knowledgetype', 'description')


    models = {
        'extractor.documentationunit': {
            'Meta': {'object_name': 'DocumentationUnit'},
            'end_offset': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'filename': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '500'}),
            'html_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parentElement': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'start_offset': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'extractor.knowledgetype': {
            'Meta': {'object_name': 'KnowledgeType'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['extractor']