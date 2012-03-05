# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'party'
        db.create_table('lintory_party', (
            ('eparty', self.gf('lintory.mfields.text_field')(db_index=True, max_length=104, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comments', self.gf('lintory.mfields.text_field')(null=True, blank=True)),
            ('name', self.gf('lintory.mfields.char_field')(max_length=30)),
        ))
        db.send_create_signal('lintory', ['party'])

        # Adding model 'history_item'
        db.create_table('lintory_history_item', (
            ('body', self.gf('lintory.mfields.text_field')(null=True, blank=True)),
            ('title', self.gf('lintory.mfields.char_field')(max_length=80)),
            ('object_pk', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='content_type_set_for_history_item', to=orm['contenttypes.ContentType'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('lintory', ['history_item'])

        # Adding model 'vendor'
        db.create_table('lintory_vendor', (
            ('name', self.gf('lintory.mfields.char_field')(max_length=30)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('telephone', self.gf('lintory.mfields.char_field')(max_length=20, null=True, blank=True)),
            ('comments', self.gf('lintory.mfields.text_field')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('lintory.mfields.text_field')(null=True, blank=True)),
            ('email', self.gf('lintory.mfields.email_field')(max_length=75, null=True, blank=True)),
        ))
        db.send_create_signal('lintory', ['vendor'])

        # Adding model 'location'
        db.create_table('lintory_location', (
            ('name', self.gf('lintory.mfields.char_field')(max_length=30)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['lintory.location'])),
            ('comments', self.gf('lintory.mfields.text_field')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='uses_locations', null=True, to=orm['lintory.party'])),
            ('address', self.gf('lintory.mfields.text_field')(null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='owns_locations', null=True, to=orm['lintory.party'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('lintory', ['location'])

        # Adding model 'hardware'
        db.create_table('lintory_hardware', (
            ('type_id', self.gf('lintory.mfields.char_field')(max_length=20)),
            ('seen_first', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_of_manufacture', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('auto_delete', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('product_number', self.gf('lintory.mfields.char_field')(max_length=30, null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='owns_hardware', null=True, to=orm['lintory.party'])),
            ('auto_model', self.gf('lintory.mfields.char_field')(db_index=True, max_length=90, null=True, blank=True)),
            ('asset_id', self.gf('lintory.mfields.char_field')(max_length=10, null=True, blank=True)),
            ('comments', self.gf('lintory.mfields.text_field')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('seen_last', self.gf('django.db.models.fields.DateTimeField')()),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lintory.location'], null=True, blank=True)),
            ('serial_number', self.gf('lintory.mfields.char_field')(max_length=50, null=True, blank=True)),
            ('installed_on', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='installed_hardware', null=True, to=orm['lintory.hardware'])),
            ('auto_serial_number', self.gf('lintory.mfields.char_field')(db_index=True, max_length=50, null=True, blank=True)),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lintory.vendor'], null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='uses_hardware', null=True, to=orm['lintory.party'])),
            ('auto_manufacturer', self.gf('lintory.mfields.char_field')(db_index=True, max_length=50, null=True, blank=True)),
            ('model', self.gf('lintory.mfields.char_field')(max_length=90, null=True, blank=True)),
            ('manufacturer', self.gf('lintory.mfields.char_field')(max_length=50, null=True, blank=True)),
            ('service_number', self.gf('lintory.mfields.char_field')(max_length=10, null=True, blank=True)),
            ('date_of_disposal', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('lintory', ['hardware'])

        # Adding model 'motherboard'
        db.create_table('lintory_motherboard', (
            ('hardware_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lintory.hardware'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('lintory', ['motherboard'])

        # Adding model 'processor'
        db.create_table('lintory_processor', (
            ('cur_speed', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('number_of_cores', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('version', self.gf('lintory.mfields.char_field')(max_length=40, null=True, blank=True)),
            ('max_speed', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hardware_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lintory.hardware'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('lintory', ['processor'])

        # Adding model 'video_controller'
        db.create_table('lintory_video_controller', (
            ('memory', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=0, blank=True)),
            ('hardware_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lintory.hardware'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('lintory', ['video_controller'])

        # Adding model 'network_adaptor'
        db.create_table('lintory_network_adaptor', (
            ('IPv4_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('mac_address', self.gf('lintory.mfields.mac_address_field')(max_length=17, db_index=True)),
            ('network_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('lintory.mfields.char_field')(max_length=100)),
            ('hardware_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lintory.hardware'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('lintory', ['network_adaptor'])

        # Adding model 'storage'
        db.create_table('lintory_storage', (
            ('total_size', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=0, blank=True)),
            ('sector_size', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('used_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='used_storage', null=True, to=orm['lintory.computer'])),
            ('signature', self.gf('lintory.mfields.char_field')(db_index=True, max_length=12, null=True, blank=True)),
            ('hardware_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lintory.hardware'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('lintory', ['storage'])

        # Adding model 'power_supply'
        db.create_table('lintory_power_supply', (
            ('watts', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_portable', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('hardware_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lintory.hardware'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('lintory', ['power_supply'])

        # Adding model 'computer'
        db.create_table('lintory_computer', (
            ('is_portable', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('memory', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=0, blank=True)),
            ('name', self.gf('lintory.mfields.char_field')(max_length=20)),
            ('hardware_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lintory.hardware'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('lintory', ['computer'])

        # Adding model 'monitor'
        db.create_table('lintory_monitor', (
            ('widescreen', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('hardware_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lintory.hardware'], unique=True, primary_key=True)),
            ('technology', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('size', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('lintory', ['monitor'])

        # Adding model 'multifunction'
        db.create_table('lintory_multifunction', (
            ('can_receive_fax', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('user_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('admin_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('windows_path', self.gf('lintory.mfields.char_field')(max_length=100, null=True, blank=True)),
            ('can_send_fax', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('accessible_on_network', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('hardware_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lintory.hardware'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('lintory', ['multifunction'])

        # Adding model 'printer'
        db.create_table('lintory_printer', (
            ('admin_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('windows_path', self.gf('lintory.mfields.char_field')(max_length=100, null=True, blank=True)),
            ('cups_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('accessible_on_network', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('colour', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('supports_Postscript', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('supports_PCL', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('technology', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('double_sided', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('hardware_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lintory.hardware'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('lintory', ['printer'])

        # Adding model 'scanner'
        db.create_table('lintory_scanner', (
            ('supports_film', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('supports_tranparencies', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('windows_path', self.gf('lintory.mfields.char_field')(max_length=100, null=True, blank=True)),
            ('user_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('admin_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('colour', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('supports_paper', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('OCR', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('accessible_on_network', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('auto_feeder', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('hardware_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lintory.hardware'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('lintory', ['scanner'])

        # Adding model 'docking_station'
        db.create_table('lintory_docking_station', (
            ('ports', self.gf('lintory.mfields.text_field')(null=True, blank=True)),
            ('hardware_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lintory.hardware'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('lintory', ['docking_station'])

        # Adding model 'camera'
        db.create_table('lintory_camera', (
            ('takes_stills', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('still_x_pixels', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('colour', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('takes_videos', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('still_y_pixels', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('video_x_pixels', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('technology', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('video_y_pixels', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('hardware_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lintory.hardware'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('lintory', ['camera'])

        # Adding model 'os'
        db.create_table('lintory_os', (
            ('name', self.gf('lintory.mfields.char_field')(max_length=40, db_index=True)),
            ('seen_first', self.gf('django.db.models.fields.DateTimeField')()),
            ('storage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lintory.storage'])),
            ('comments', self.gf('lintory.mfields.text_field')(null=True, blank=True)),
            ('seen_last', self.gf('django.db.models.fields.DateTimeField')()),
            ('computer_name', self.gf('lintory.mfields.char_field')(max_length=20, db_index=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('lintory', ['os'])

        # Adding model 'software'
        db.create_table('lintory_software', (
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lintory.vendor'], null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comments', self.gf('lintory.mfields.text_field')(null=True, blank=True)),
            ('name', self.gf('lintory.mfields.char_field')(max_length=100)),
        ))
        db.send_create_signal('lintory', ['software'])

        # Adding model 'license'
        db.create_table('lintory_license', (
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lintory.vendor'], null=True, blank=True)),
            ('installations_max', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('text', self.gf('lintory.mfields.text_field')(null=True, blank=True)),
            ('expires', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('comments', self.gf('lintory.mfields.text_field')(null=True, blank=True)),
            ('version', self.gf('lintory.mfields.char_field')(max_length=20, null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='owns_licenses', null=True, to=orm['lintory.party'])),
            ('vendor_tag', self.gf('lintory.mfields.char_field')(max_length=10, null=True, blank=True)),
            ('computer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lintory.computer'], null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('lintory.mfields.char_field')(db_index=True, max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('lintory', ['license'])

        # Adding model 'license_key'
        db.create_table('lintory_license_key', (
            ('key', self.gf('lintory.mfields.char_field')(db_index=True, max_length=50, null=True, blank=True)),
            ('comments', self.gf('lintory.mfields.text_field')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('license', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lintory.license'])),
            ('software', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lintory.software'])),
        ))
        db.send_create_signal('lintory', ['license_key'])

        # Adding model 'software_installation'
        db.create_table('lintory_software_installation', (
            ('software_version', self.gf('lintory.mfields.char_field')(max_length=20, null=True, blank=True)),
            ('seen_first', self.gf('django.db.models.fields.DateTimeField')()),
            ('auto_license_key', self.gf('lintory.mfields.char_field')(max_length=50, null=True, blank=True)),
            ('auto_delete', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('comments', self.gf('lintory.mfields.text_field')(null=True, blank=True)),
            ('seen_last', self.gf('django.db.models.fields.DateTimeField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('license_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lintory.license_key'], null=True, blank=True)),
            ('os', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lintory.os'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('software', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lintory.software'])),
        ))
        db.send_create_signal('lintory', ['software_installation'])

        # Adding model 'task'
        db.create_table('lintory_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comments', self.gf('lintory.mfields.text_field')(null=True, blank=True)),
            ('name', self.gf('lintory.mfields.char_field')(max_length=40)),
        ))
        db.send_create_signal('lintory', ['task'])

        # Adding model 'hardware_task'
        db.create_table('lintory_hardware_task', (
            ('assigned', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='assigned_hardware_tasks', null=True, to=orm['lintory.party'])),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lintory.task'])),
            ('comments', self.gf('lintory.mfields.text_field')(null=True, blank=True)),
            ('hardware', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lintory.hardware'])),
            ('date_complete', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('lintory', ['hardware_task'])

        # Adding model 'data'
        db.create_table('lintory_data', (
            ('create_os', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('errors', self.gf('lintory.mfields.text_field')(null=True, blank=True)),
            ('imported', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('format', self.gf('lintory.mfields.char_field')(max_length=10)),
            ('comments', self.gf('lintory.mfields.text_field')(null=True, blank=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('computer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lintory.computer'], null=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('create_computer', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('os', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lintory.os'], null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_attempt', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('lintory', ['data'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'party'
        db.delete_table('lintory_party')

        # Deleting model 'history_item'
        db.delete_table('lintory_history_item')

        # Deleting model 'vendor'
        db.delete_table('lintory_vendor')

        # Deleting model 'location'
        db.delete_table('lintory_location')

        # Deleting model 'hardware'
        db.delete_table('lintory_hardware')

        # Deleting model 'motherboard'
        db.delete_table('lintory_motherboard')

        # Deleting model 'processor'
        db.delete_table('lintory_processor')

        # Deleting model 'video_controller'
        db.delete_table('lintory_video_controller')

        # Deleting model 'network_adaptor'
        db.delete_table('lintory_network_adaptor')

        # Deleting model 'storage'
        db.delete_table('lintory_storage')

        # Deleting model 'power_supply'
        db.delete_table('lintory_power_supply')

        # Deleting model 'computer'
        db.delete_table('lintory_computer')

        # Deleting model 'monitor'
        db.delete_table('lintory_monitor')

        # Deleting model 'multifunction'
        db.delete_table('lintory_multifunction')

        # Deleting model 'printer'
        db.delete_table('lintory_printer')

        # Deleting model 'scanner'
        db.delete_table('lintory_scanner')

        # Deleting model 'docking_station'
        db.delete_table('lintory_docking_station')

        # Deleting model 'camera'
        db.delete_table('lintory_camera')

        # Deleting model 'os'
        db.delete_table('lintory_os')

        # Deleting model 'software'
        db.delete_table('lintory_software')

        # Deleting model 'license'
        db.delete_table('lintory_license')

        # Deleting model 'license_key'
        db.delete_table('lintory_license_key')

        # Deleting model 'software_installation'
        db.delete_table('lintory_software_installation')

        # Deleting model 'task'
        db.delete_table('lintory_task')

        # Deleting model 'hardware_task'
        db.delete_table('lintory_hardware_task')

        # Deleting model 'data'
        db.delete_table('lintory_data')
    
    
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
            'hardware_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lintory.hardware']", 'unique': 'True', 'primary_key': 'True'})
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
            'IPv4_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
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
