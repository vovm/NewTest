# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'AllRequest.priority'
        db.add_column(u'hello_allrequest', 'priority',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'AllRequest.priority'
        db.delete_column(u'hello_allrequest', 'priority')


    models = {
        u'hello.about': {
            'Meta': {'object_name': 'About'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'other_contact': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'hello.allrequest': {
            'Meta': {'object_name': 'AllRequest'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'})
        },
        u'hello.signaldata': {
            'Meta': {'object_name': 'SignalData'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['hello']