# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Line.destination_name'
        db.delete_column('transit_line', 'destination_name')


    def backwards(self, orm):
        # Adding field 'Line.destination_name'
        db.add_column('transit_line', 'destination_name',
                      self.gf('django.db.models.fields.CharField')(default='Lala land', max_length=100),
                      keep_default=False)


    models = {
        'transit.bus': {
            'Meta': {'object_name': 'Bus'},
            'arrival_times': ('django.db.models.fields.TextField', [], {}),
            'delay': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '6'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['transit.Line']"}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '6'})
        },
        'transit.line': {
            'Meta': {'object_name': 'Line'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'opposite_line': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['transit.Line']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'transit.linestoplink': {
            'Meta': {'object_name': 'LineStopLink'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['transit.Line']"}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['transit.Stop']"})
        },
        'transit.stop': {
            'Meta': {'object_name': 'Stop'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '6'}),
            'lines': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'stops'", 'symmetrical': 'False', 'through': "orm['transit.LineStopLink']", 'to': "orm['transit.Line']"}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '6'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['transit']