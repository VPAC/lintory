from lintory import eparty
from django.db import models
from django import forms

class name_widget(forms.widgets.TextInput):

    def render(self, name, value, attrs=None):
        if isinstance(value, eparty.backend.Name_Base):
                value = value.get_id()
        return super(name_widget, self).render(name, value, attrs)


class name_form_field(forms.CharField):
    widget = name_widget

    def __init__(self, *args, **kwargs):
        super(name_form_field, self).__init__(*args, **kwargs)

    def clean(self, value):      
        value=super(name_form_field, self).clean(value)

        if value in ('',None):
            return None

        try:
            n = eparty.connection.lookup_user_input(value)
        except eparty.Not_Found_Error, e:
            raise forms.util.ValidationError(u"Cannot find name %s: %s" % (value,e))

        return n


class Error_Name(eparty.backend.Name_Base):
    data = None

    def __init__(self,data):
        self.data = data

    def get_id(self):
        return self.data

    def is_in_group(self,group):
        return False

class name_model_field(models.CharField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 104
        super(name_model_field, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, eparty.backend.Name_Base):
            return value

        if value is None:
            return None

        try:
            n = eparty.connection.lookup_id(value)
        except eparty.Not_Found_Error, e:
            return Error_Name(value)

        return n

    def get_db_prep_value(self, value):
        if value is None:
            return None

        return value.get_id()

    def get_db_prep_lookup(self, lookup_type, value, connection, prepared=False):
        if lookup_type == 'exact':
            return [self.get_db_prep_value(value)]
        elif lookup_type == 'in':
            return [self.get_db_prep_value(v) for v in value]
        elif lookup_type == 'isnull':
            return []
        else:
            raise TypeError('Lookup type %r not supported.' % lookup_type)

    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {'form_class': name_form_field}
        defaults.update(kwargs)
        return super(name_model_field, self).formfield(**defaults)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^lintory\.eparty\.fields\.name_model_field$"])
