# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DocumentationUnit'
        db.create_table('pythondocwebsite_documentationunit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('checked', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal('pythondocwebsite', ['DocumentationUnit'])


    def backwards(self, orm):
        # Deleting model 'DocumentationUnit'
        db.delete_table('pythondocwebsite_documentationunit')


    models = {
        'pythondocwebsite.documentationunit': {
            'Meta': {'object_name': 'DocumentationUnit'},
            'checked': ('django.db.models.fields.BooleanField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['pythondocwebsite']