# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ParentElement'
        db.create_table('extractor_parentelement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('html_text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('extractor', ['ParentElement'])


        # Renaming column for 'DocumentationUnit.parentElement' to match new field type.
        db.rename_column('extractor_documentationunit', 'parentElement', 'parentElement_id')
        # Changing field 'DocumentationUnit.parentElement'
        db.alter_column('extractor_documentationunit', 'parentElement_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['extractor.ParentElement']))
        # Adding index on 'DocumentationUnit', fields ['parentElement']
        db.create_index('extractor_documentationunit', ['parentElement_id'])


    def backwards(self, orm):
        # Removing index on 'DocumentationUnit', fields ['parentElement']
        db.delete_index('extractor_documentationunit', ['parentElement_id'])

        # Deleting model 'ParentElement'
        db.delete_table('extractor_parentelement')


        # Renaming column for 'DocumentationUnit.parentElement' to match new field type.
        db.rename_column('extractor_documentationunit', 'parentElement_id', 'parentElement')
        # Changing field 'DocumentationUnit.parentElement'
        db.alter_column('extractor_documentationunit', 'parentElement', self.gf('django.db.models.fields.IntegerField')())

    models = {
        'extractor.documentationunit': {
            'Meta': {'object_name': 'DocumentationUnit'},
            'end_offset': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'filename': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '500'}),
            'html_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parentElement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['extractor.ParentElement']"}),
            'start_offset': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'extractor.knowledgetype': {
            'Meta': {'object_name': 'KnowledgeType'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'extractor.parentelement': {
            'Meta': {'object_name': 'ParentElement'},
            'html_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['extractor']