from django import forms
import lintory.fields as fields
import lintory.models as models

class party_form(forms.ModelForm):

    class Meta:
        model = models.party

class history_item_form(forms.ModelForm):

    class Meta:
        model = models.history_item
        exclude = ('list','date','content_type','object_pk')

class history_item_form_with_date(forms.ModelForm):

    class Meta:
        model = models.history_item
        exclude = ('list','content_type','object_pk')

class vendor_form(forms.ModelForm):

    class Meta:
        model = models.vendor

class hardware_task_form(forms.ModelForm):
    assigned     = fields.party_field(required=False)

    class Meta:
        model = models.hardware_task

class location_form(forms.ModelForm):
    owner    = fields.party_field(required=False)
    user     = fields.party_field(required=False)

    class Meta:
        model = models.location

class task_form(forms.ModelForm):

    class Meta:
        model = models.task

class hardware_form(forms.ModelForm):
    owner    = fields.party_field(required=False)
    user     = fields.party_field(required=False)

    class Meta:
        model = models.hardware
        exclude = ('type_id', 'auto_delete', 'auto_manufacturer', 'auto_model', 'auto_serial_number' )

class motherboard_form(hardware_form):
    class Meta:
        model = models.motherboard
        exclude = ('type_id', 'auto_delete', 'auto_manufacturer', 'auto_model', 'auto_serial_number' )

class processor_form(hardware_form):
    class Meta:
        model = models.processor
        exclude = ('type_id', 'auto_delete', 'auto_manufacturer', 'auto_model', 'auto_serial_number' )

class video_controller_form(hardware_form):
    class Meta:
        model = models.video_controller
        exclude = ('type_id', 'auto_delete', 'auto_manufacturer', 'auto_model', 'auto_serial_number' )

class network_adaptor_form(hardware_form):
    class Meta:
        model = models.network_adaptor
        exclude = ('type_id', 'auto_delete', 'auto_manufacturer', 'auto_model', 'auto_serial_number' )

class storage_form(hardware_form):
    class Meta:
        model = models.storage
        exclude = ('type_id', 'auto_delete', 'auto_manufacturer', 'auto_model', 'auto_serial_number' )

class power_supply_form(hardware_form):
    class Meta:
        model = models.power_supply
        exclude = ('type_id', 'auto_delete', 'auto_manufacturer', 'auto_model', 'auto_serial_number' )

class computer_form(hardware_form):
    class Meta:
        model = models.computer
        exclude = ('type_id', 'auto_delete', 'auto_manufacturer', 'auto_model', 'auto_serial_number' )

class monitor_form(hardware_form):
    class Meta:
        model = models.monitor
        exclude = ('type_id', 'auto_delete', 'auto_manufacturer', 'auto_model', 'auto_serial_number' )

class os_form(forms.ModelForm):
    class Meta:
        model = models.os

class software_form(forms.ModelForm):

    class Meta:
        model = models.software

class license_form(forms.ModelForm):
    owner    = fields.party_field(required=False)

    class Meta:
        model = models.license

class license_key_form(forms.ModelForm):

    class Meta:
        model = models.license_key

class software_installation_form(forms.ModelForm):

    class Meta:
        model = models.software_installation
        exclude = ('license_key','auto_delete','auto_license_key')

class license_key_select_form(forms.Form):
    key = forms.ChoiceField(required=False)

    def __init__(self, software, *args, **kwargs):
        super(license_key_select_form, self).__init__(*args,**kwargs)

        keys = models.license_key.objects.filter(software=software)
        choices = [ (lk.id,lk) for lk in keys ]
        choices.insert( 0, ("","None") )
        self.fields['key'].choices = choices

class license_create_form(forms.Form):
    vendor_tag = fields.char_field(max_length=10,required=False)
    installations_max = forms.IntegerField(min_value=0,required=False)
    version    = fields.char_field(max_length=20,required=False)
    expires = forms.DateTimeField(required=False)
    owner    = fields.party_field(required=False)
    key = fields.char_field(max_length=50)

class data_form(forms.ModelForm):

    class Meta:
        model = models.data
        exclude = ('errors',)
