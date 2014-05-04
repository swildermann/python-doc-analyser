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

        # Adding model 'DocumentationUnit'
        db.create_table('extractor_documentationunit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('html_text', self.gf('django.db.models.fields.TextField')()),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=500, default='None')),
            ('start_offset', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('end_offset', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('extractor', ['DocumentationUnit'])

        # Adding model 'KnowledgeType'
        db.create_table('extractor_knowledgetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('extractor', ['KnowledgeType'])

        # Adding model 'MarkedUnit'
        db.create_table('extractor_markedunit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True, null=True)),
            ('documentation_unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['extractor.DocumentationUnit'])),
            ('knowledge_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('html_text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('extractor', ['MarkedUnit'])


    def backwards(self, orm):
        # Deleting model 'ParentElement'
        db.delete_table('extractor_parentelement')

        # Deleting model 'DocumentationUnit'
        db.delete_table('extractor_documentationunit')

        # Deleting model 'KnowledgeType'
        db.delete_table('extractor_knowledgetype')

        # Deleting model 'MarkedUnit'
        db.delete_table('extractor_markedunit')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True', 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'extractor.documentationunit': {
            'Meta': {'object_name': 'DocumentationUnit'},
            'end_offset': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "'None'"}),
            'html_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_offset': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'extractor.knowledgetype': {
            'Meta': {'object_name': 'KnowledgeType'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'extractor.markedunit': {
            'Meta': {'object_name': 'MarkedUnit'},
            'documentation_unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['extractor.DocumentationUnit']"}),
            'html_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'knowledge_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True', 'null': 'True'})
        },
        'extractor.parentelement': {
            'Meta': {'object_name': 'ParentElement'},
            'html_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['extractor']