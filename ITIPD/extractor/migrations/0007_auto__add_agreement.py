# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Agreement'
        db.create_table('extractor_agreement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first', self.gf('django.db.models.fields.related.ForeignKey')(related_name='first', to=orm['extractor.MappingUnitToUser'])),
            ('second', self.gf('django.db.models.fields.related.ForeignKey')(related_name='second', to=orm['extractor.MappingUnitToUser'])),
            ('percentage_by_types', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('percentage_by_chars', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('extractor', ['Agreement'])


    def backwards(self, orm):
        # Deleting model 'Agreement'
        db.delete_table('extractor_agreement')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'related_name': "'user_set'", 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'related_name': "'user_set'", 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'ordering': "('name',)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'extractor.accesslog': {
            'Meta': {'object_name': 'AccessLog'},
            'documentation_unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['extractor.DocumentationUnit']"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"})
        },
        'extractor.agreement': {
            'Meta': {'object_name': 'Agreement'},
            'first': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first'", 'to': "orm['extractor.MappingUnitToUser']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage_by_chars': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'percentage_by_types': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'second': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'second'", 'to': "orm['extractor.MappingUnitToUser']"})
        },
        'extractor.documentationunit': {
            'Meta': {'object_name': 'DocumentationUnit'},
            'file_text': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "'None'"}),
            'html_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'offset': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'parent_text': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'plaintext': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "''"})
        },
        'extractor.knowledgetype': {
            'Meta': {'object_name': 'KnowledgeType'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'extractor.mappingunittouser': {
            'Meta': {'object_name': 'MappingUnitToUser'},
            'already_marked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'documentation_unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['extractor.DocumentationUnit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_change': ('django.db.models.fields.DateTimeField', [], {'default': '0'}),
            'unmarked_chars': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unmarked_percent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"})
        },
        'extractor.markedunit': {
            'Meta': {'object_name': 'MarkedUnit'},
            'char_range': ('django.db.models.fields.TextField', [], {'max_length': '500', 'default': "''"}),
            'documentation_unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['extractor.DocumentationUnit']"}),
            'html_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'knowledge_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'range': ('django.db.models.fields.TextField', [], {'max_length': '500', 'default': "''"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['extractor']