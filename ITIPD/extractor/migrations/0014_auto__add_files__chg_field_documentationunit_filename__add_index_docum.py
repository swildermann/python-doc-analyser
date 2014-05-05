# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Files'
        db.create_table('extractor_files', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=500, default='None')),
            ('html_text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('extractor', ['Files'])


        # Renaming column for 'DocumentationUnit.filename' to match new field type.
        db.rename_column('extractor_documentationunit', 'filename', 'filename_id')
        # Changing field 'DocumentationUnit.filename'
        db.alter_column('extractor_documentationunit', 'filename_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['extractor.Files']))
        # Adding index on 'DocumentationUnit', fields ['filename']
        db.create_index('extractor_documentationunit', ['filename_id'])


        # Changing field 'MappingUnitToUser.user'
        db.alter_column('extractor_mappingunittouser', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

    def backwards(self, orm):
        # Removing index on 'DocumentationUnit', fields ['filename']
        db.delete_index('extractor_documentationunit', ['filename_id'])

        # Deleting model 'Files'
        db.delete_table('extractor_files')


        # Renaming column for 'DocumentationUnit.filename' to match new field type.
        db.rename_column('extractor_documentationunit', 'filename_id', 'filename')
        # Changing field 'DocumentationUnit.filename'
        db.alter_column('extractor_documentationunit', 'filename', self.gf('django.db.models.fields.CharField')(max_length=500))

        # Changing field 'MappingUnitToUser.user'
        db.alter_column('extractor_mappingunittouser', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'extractor.documentationunit': {
            'Meta': {'object_name': 'DocumentationUnit'},
            'filename': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['extractor.Files']"}),
            'html_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'extractor.files': {
            'Meta': {'object_name': 'Files'},
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '500', 'default': "'None'"}),
            'html_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'default': "'sven'"})
        },
        'extractor.markedunit': {
            'Meta': {'object_name': 'MarkedUnit'},
            'documentation_unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['extractor.DocumentationUnit']"}),
            'html_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'knowledge_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'range': ('django.db.models.fields.TextField', [], {'max_length': '500', 'default': "''"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"})
        },
        'extractor.parentelement': {
            'Meta': {'object_name': 'ParentElement'},
            'html_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['extractor']