# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'party.LDAP_DN'
        db.add_column('lintory_party', 'LDAP_DN', self.gf('lintory.mfields.char_field')(db_index=True, max_length=104, null=True, blank=True), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'party.LDAP_DN'
        db.delete_column('lintory_party', 'LDAP_DN')
    
    
    models = {
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'lintory.camera': {
            'Meta': {'object_name': 'camera', '_ormbases': ['lintory.hardware']},
            'colour': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'hardware_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lintory.hardware']", 'unique': 'True', 'primary_key': 'True'}),
            'still_x_pixels': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'still_y_pixels': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'takes_stills': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'takes_videos': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'technology': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'video_x_pixels': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_y_pixels': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'lintory.computer': {
            'Meta': {'object_name': 'computer', '_ormbases': ['lintory.hardware']},
            'hardware_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lintory.hardware']", 'unique': 'True', 'primary_key': 'True'}),
            'is_portable': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'memory': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '0', 'blank': 'True'}),
            'name': ('lintory.mfields.char_field', [], {'max_length': '20'})
        },
        'lintory.data': {
            'Meta': {'object_name': 'data'},
            'comments': ('lintory.mfields.text_field', [], {'null': 'True', 'blank': 'True'}),
            'computer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lintory.computer']", 'null': 'True', 'blank': 'True'}),
            'create_computer': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'create_os': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'errors': ('lintory.mfields.text_field', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'format': ('lintory.mfields.char_field', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imported': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_attempt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'os': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lintory.os']", 'null': 'True', 'blank': 'True'})
        },
        'lintory.docking_station': {
            'Meta': {'object_name': 'docking_station', '_ormbases': ['lintory.hardware']},
            'hardware_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lintory.hardware']", 'unique': 'True', 'primary_key': 'True'}),
            'ports': ('lintory.mfields.text_field', [], {'null': 'True', 'blank': 'True'})
        },
        'lintory.hardware': {
            'Meta': {'object_name': 'hardware'},
            'asset_id': ('lintory.mfields.char_field', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'auto_delete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'auto_manufacturer': ('lintory.mfields.char_field', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'auto_model': ('lintory.mfields.char_field', [], {'db_index': 'True', 'max_length': '90', 'null': 'True', 'blank': 'True'}),
            'auto_serial_number': ('lintory.mfields.char_field', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'comments': ('lintory.mfields.text_field', [], {'null': 'True', 'blank': 'True'}),
            'date_of_disposal': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_of_manufacture': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'installed_on': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'installed_hardware'", 'null': 'True', 'to': "orm['lintory.hardware']"}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lintory.location']", 'null': 'True', 'blank': 'True'}),
            'manufacturer': ('lintory.mfields.char_field', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'model': ('lintory.mfields.char_field', [], {'max_length': '90', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owns_hardware'", 'null': 'True', 'to': "orm['lintory.party']"}),
            'product_number': ('lintory.mfields.char_field', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'seen_first': ('django.db.models.fields.DateTimeField', [], {}),
            'seen_last': ('django.db.models.fields.DateTimeField', [], {}),
            'serial_number': ('lintory.mfields.char_field', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'service_number': ('lintory.mfields.char_field', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'type_id': ('lintory.mfields.char_field', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'uses_hardware'", 'null': 'True', 'to': "orm['lintory.party']"}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lintory.vendor']", 'null': 'True', 'blank': 'True'})
        },
        'lintory.hardware_task': {
            'Meta': {'object_name': 'hardware_task'},
            'assigned': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'assigned_hardware_tasks'", 'null': 'True', 'to': "orm['lintory.party']"}),
            'comments': ('lintory.mfields.text_field', [], {'null': 'True', 'blank': 'True'}),
            'date_complete': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'hardware': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lintory.hardware']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lintory.task']"})
        },
        'lintory.history_item': {
            'Meta': {'object_name': 'history_item'},
            'body': ('lintory.mfields.text_field', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_history_item'", 'to': "orm['contenttypes.ContentType']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_pk': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('lintory.mfields.char_field', [], {'max_length': '80'})
        },
        'lintory.license': {
            'Meta': {'object_name': 'license'},
            'comments': ('lintory.mfields.text_field', [], {'null': 'True', 'blank': 'True'}),
            'computer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lintory.computer']", 'null': 'True', 'blank': 'True'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'installations_max': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('lintory.mfields.char_field', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owns_licenses'", 'null': 'True', 'to': "orm['lintory.party']"}),
            'text': ('lintory.mfields.text_field', [], {'null': 'True', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lintory.vendor']", 'null': 'True', 'blank': 'True'}),
            'vendor_tag': ('lintory.mfields.char_field', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'version': ('lintory.mfields.char_field', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'lintory.license_key': {
            'Meta': {'object_name': 'license_key'},
            'comments': ('lintory.mfields.text_field', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('lintory.mfields.char_field', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lintory.license']"}),
            'software': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lintory.software']"})
        },
        'lintory.location': {
            'Meta': {'object_name': 'location'},
            'address': ('lintory.mfields.text_field', [], {'null': 'True', 'blank': 'True'}),
            'comments': ('lintory.mfields.text_field', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('lintory.mfields.char_field', [], {'max_length': '30'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owns_locations'", 'null': 'True', 'to': "orm['lintory.party']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['lintory.location']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'uses_locations'", 'null': 'True', 'to': "orm['lintory.party']"})
        },
        'lintory.monitor': {
            'Meta': {'object_name': 'monitor', '_ormbases': ['lintory.hardware']},
            'hardware_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lintory.hardware']", 'unique': 'True', 'primary_key': 'True'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'technology': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'widescreen': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'lintory.motherboard': {
            'Meta': {'object_name': 'motherboard', '_ormbases': ['lintory.hardware']},
            'hardware_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lintory.hardware']", 'unique': 'True', 'primary_key': 'True'}),
            'type': ('lintory.mfields.char_field', [], {'max_length': '20'})
        },
        'lintory.multifunction': {
            'Meta': {'object_name': 'multifunction', '_ormbases': ['lintory.hardware']},
            'accessible_on_network': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'admin_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'can_receive_fax': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'can_send_fax': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'hardware_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lintory.hardware']", 'unique': 'True', 'primary_key': 'True'}),
            'user_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'windows_path': ('lintory.mfields.char_field', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'lintory.network_adaptor': {
            'Meta': {'object_name': 'network_adaptor', '_ormbases': ['lintory.hardware']},
            'hardware_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lintory.hardware']", 'unique': 'True', 'primary_key': 'True'}),
            'mac_address': ('lintory.mfields.mac_address_field', [], {'max_length': '17', 'db_index': 'True'}),
            'name': ('lintory.mfields.char_field', [], {'max_length': '100'}),
            'network_type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'lintory.os': {
            'Meta': {'object_name': 'os'},
            'comments': ('lintory.mfields.text_field', [], {'null': 'True', 'blank': 'True'}),
            'computer_name': ('lintory.mfields.char_field', [], {'max_length': '20', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('lintory.mfields.char_field', [], {'max_length': '40', 'db_index': 'True'}),
            'seen_first': ('django.db.models.fields.DateTimeField', [], {}),
            'seen_last': ('django.db.models.fields.DateTimeField', [], {}),
            'storage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lintory.storage']"})
        },
        'lintory.party': {
            'LDAP_DN': ('lintory.mfields.char_field', [], {'db_index': 'True', 'max_length': '104', 'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'party'},
            'comments': ('lintory.mfields.text_field', [], {'null': 'True', 'blank': 'True'}),
            'eparty': ('lintory.mfields.char_field', [], {'db_index': 'True', 'max_length': '104', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('lintory.mfields.char_field', [], {'max_length': '30'})
        },
        'lintory.power_supply': {
            'Meta': {'object_name': 'power_supply', '_ormbases': ['lintory.hardware']},
            'hardware_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lintory.hardware']", 'unique': 'True', 'primary_key': 'True'}),
            'is_portable': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'watts': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'lintory.printer': {
            'Meta': {'object_name': 'printer', '_ormbases': ['lintory.hardware']},
            'accessible_on_network': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'admin_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'colour': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'cups_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'double_sided': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'hardware_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lintory.hardware']", 'unique': 'True', 'primary_key': 'True'}),
            'supports_PCL': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'supports_Postscript': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'technology': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'windows_path': ('lintory.mfields.char_field', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'lintory.processor': {
            'Meta': {'object_name': 'processor', '_ormbases': ['lintory.hardware']},
            'cur_speed': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hardware_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lintory.hardware']", 'unique': 'True', 'primary_key': 'True'}),
            'max_speed': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'number_of_cores': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'version': ('lintory.mfields.char_field', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        },
        'lintory.scanner': {
            'Meta': {'object_name': 'scanner', '_ormbases': ['lintory.hardware']},
            'OCR': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'accessible_on_network': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'admin_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'auto_feeder': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'colour': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'hardware_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lintory.hardware']", 'unique': 'True', 'primary_key': 'True'}),
            'supports_film': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'supports_paper': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'supports_tranparencies': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'user_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'windows_path': ('lintory.mfields.char_field', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'lintory.software': {
            'Meta': {'object_name': 'software'},
            'comments': ('lintory.mfields.text_field', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('lintory.mfields.char_field', [], {'max_length': '100'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lintory.vendor']", 'null': 'True', 'blank': 'True'})
        },
        'lintory.software_installation': {
            'Meta': {'object_name': 'software_installation'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'auto_delete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'auto_license_key': ('lintory.mfields.char_field', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'comments': ('lintory.mfields.text_field', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lintory.license_key']", 'null': 'True', 'blank': 'True'}),
            'os': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lintory.os']"}),
            'seen_first': ('django.db.models.fields.DateTimeField', [], {}),
            'seen_last': ('django.db.models.fields.DateTimeField', [], {}),
            'software': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lintory.software']"}),
            'software_version': ('lintory.mfields.char_field', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'lintory.storage': {
            'Meta': {'object_name': 'storage', '_ormbases': ['lintory.hardware']},
            'hardware_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lintory.hardware']", 'unique': 'True', 'primary_key': 'True'}),
            'sector_size': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'signature': ('lintory.mfields.char_field', [], {'db_index': 'True', 'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'total_size': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '0', 'blank': 'True'}),
            'used_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'used_storage'", 'null': 'True', 'to': "orm['lintory.computer']"})
        },
        'lintory.task': {
            'Meta': {'object_name': 'task'},
            'comments': ('lintory.mfields.text_field', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('lintory.mfields.char_field', [], {'max_length': '40'})
        },
        'lintory.vendor': {
            'Meta': {'object_name': 'vendor'},
            'address': ('lintory.mfields.text_field', [], {'null': 'True', 'blank': 'True'}),
            'comments': ('lintory.mfields.text_field', [], {'null': 'True', 'blank': 'True'}),
            'email': ('lintory.mfields.email_field', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('lintory.mfields.char_field', [], {'max_length': '30'}),
            'telephone': ('lintory.mfields.char_field', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'lintory.video_controller': {
            'Meta': {'object_name': 'video_controller', '_ormbases': ['lintory.hardware']},
            'hardware_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lintory.hardware']", 'unique': 'True', 'primary_key': 'True'}),
            'memory': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '0', 'blank': 'True'})
        }
    }
    
    complete_apps = ['lintory']
