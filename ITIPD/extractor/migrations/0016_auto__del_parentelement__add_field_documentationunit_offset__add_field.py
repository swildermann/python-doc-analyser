# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ParentElement'
        db.delete_table('extractor_parentelement')

        # Adding field 'DocumentationUnit.offset'
        db.add_column('extractor_documentationunit', 'offset',
                      self.gf('django.db.models.fields.IntegerField')(default=-1),
                      keep_default=False)

        # Adding field 'DocumentationUnit.parent_text'
        db.add_column('extractor_documentationunit', 'parent_text',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'DocumentationUnit.file_text'
        db.add_column('extractor_documentationunit', 'file_text',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'ParentElement'
        db.create_table('extractor_parentelement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('html_text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('extractor', ['ParentElement'])

        # Deleting field 'DocumentationUnit.offset'
        db.delete_column('extractor_documentationunit', 'offset')

        # Deleting field 'DocumentationUnit.parent_text'
        db.delete_column('extractor_documentationunit', 'parent_text')

        # Deleting field 'DocumentationUnit.file_text'
        db.delete_column('extractor_documentationunit', 'file_text')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'ordering': "('name',)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'extractor.documentationunit': {
            'Meta': {'object_name': 'DocumentationUnit'},
            'file_text': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "'None'"}),
            'html_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'offset': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'parent_text': ('django.db.models.fields.TextField', [], {'default': "''"})
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"})
        },
        'extractor.markedunit': {
            'Meta': {'object_name': 'MarkedUnit'},
            'documentation_unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['extractor.DocumentationUnit']"}),
            'html_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'knowledge_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'range': ('django.db.models.fields.TextField', [], {'max_length': '500', 'default': "''"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['extractor']