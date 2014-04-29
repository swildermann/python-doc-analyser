# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DocumentationUnit'
        db.create_table('extractor_documentationunit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('html_text', self.gf('django.db.models.fields.TextField')()),
            ('parentElement', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('filename', self.gf('django.db.models.fields.CharField')(default=None, max_length=500)),
            ('start_offset', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('end_offset', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('extractor', ['DocumentationUnit'])

        # Adding model 'KnowledgeType'
        db.create_table('extractor_knowledgetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('desription', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('extractor', ['KnowledgeType'])


    def backwards(self, orm):
        # Deleting model 'DocumentationUnit'
        db.delete_table('extractor_documentationunit')

        # Deleting model 'KnowledgeType'
        db.delete_table('extractor_knowledgetype')


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
            'desription': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['extractor']