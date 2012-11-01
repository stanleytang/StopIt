# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Bus'
        db.create_table('transit_bus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('line', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transit.Line'])),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=6)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=6)),
            ('arrival_times', self.gf('django.db.models.fields.TextField')()),
            ('delay', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('transit', ['Bus'])

        # Adding model 'Line'
        db.create_table('transit_line', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('opposite_line', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['transit.Line'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('transit', ['Line'])

        # Adding model 'LineStopLink'
        db.create_table('transit_linestoplink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('line', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transit.Line'])),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transit.Stop'])),
            ('index', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('transit', ['LineStopLink'])

        # Adding model 'Stop'
        db.create_table('transit_stop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=6)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=6)),
        ))
        db.send_create_signal('transit', ['Stop'])


    def backwards(self, orm):
        # Deleting model 'Bus'
        db.delete_table('transit_bus')

        # Deleting model 'Line'
        db.delete_table('transit_line')

        # Deleting model 'LineStopLink'
        db.delete_table('transit_linestoplink')

        # Deleting model 'Stop'
        db.delete_table('transit_stop')


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