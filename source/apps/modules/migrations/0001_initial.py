# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Manufacturer'
        db.create_table('modules_manufacturer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('modules', ['Manufacturer'])

        # Adding model 'Module'
        db.create_table('modules_module', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['modules.Manufacturer'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('hp', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('depth', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('current_12v', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('negative_current_12v', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('current_5v', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('modules', ['Module'])


    def backwards(self, orm):
        # Deleting model 'Manufacturer'
        db.delete_table('modules_manufacturer')

        # Deleting model 'Module'
        db.delete_table('modules_module')


    models = {
        'modules.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'modules.module': {
            'Meta': {'object_name': 'Module'},
            'current_12v': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'current_5v': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'depth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['modules.Manufacturer']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'negative_current_12v': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['modules']