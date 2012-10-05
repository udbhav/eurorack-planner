# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Module.msrp'
        db.add_column('modules_module', 'msrp',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Module.msrp'
        db.delete_column('modules_module', 'msrp')


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
            'msrp': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'negative_current_12v': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['modules']