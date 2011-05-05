# lintory - keep track of computers and licenses
# Copyright (C) 2008-2009 Brian May
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.forms.util import ValidationError
from django.utils.translation import ugettext as _
from django import forms
from django.utils.encoding import smart_unicode

import lintory.models as models
import re

import pyparsing as p

import ajax_select.fields

class select_widget(ajax_select.fields.AutoCompleteSelectWidget):
    class Media:
        css = {
            'all': ( 'css/jquery.autocomplete.css', )
        }
        js = ('js/jquery.js','js/jquery.autocomplete.js',)

class select_field(ajax_select.fields.AutoCompleteSelectField):

    def __init__(self, channel, *args, **kwargs):
        widget = kwargs.get("widget", None)
        if widget is None:
            kwargs["widget"] = select_widget(channel=channel,help_text=kwargs.get('help_text',_('Enter text to search.')))
        super(select_field, self).__init__(channel, *args, **kwargs)

class select_multiple_widget(ajax_select.fields.AutoCompleteSelectMultipleWidget):
    class Media:
        css = {
            'all': ( 'css/jquery.autocomplete.css', )
        }
        js = ('js/jquery.js','js/jquery.autocomplete.js',)

class select_multiple_field(ajax_select.fields.AutoCompleteSelectMultipleField):

    def __init__(self, channel, *args, **kwargs):
        widget = kwargs.get("widget", None)
        if widget is None:
            kwargs["widget"] = select_widget(channel=channel,help_text=kwargs.get('help_text',_('Enter text to search.')))
        super(select_multiple_field, self).__init__(channel, *args, **kwargs)

class object_widget(forms.widgets.TextInput):

    def __init__(self, object_class, *args, **kwargs):
        self.object_class = object_class
        return super(object_widget,self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if isinstance(value, (int,long,)):
            object = self.object_class.objects.get(pk=value)
            value = smart_unicode(object)
        return super(object_widget,self).render(name, value, attrs)

class object_name_field(forms.CharField):

    def __init__(self, object_class, *args, **kwargs):
        self.object_class = object_class
        kwargs['widget'] = object_widget(models.party)
        super(object_name_field, self).__init__(*args, **kwargs)

    def clean(self, value):
        value=super(object_name_field, self).clean(value)

        if value in ('',None):
            return None

        try:
            clean=self.object_class.objects.get(name=value)
        except self.object_class.DoesNotExist, e:
            raise ValidationError(u"Cannot find object %s: %s" % (value,e))

        return clean

class char_field(forms.CharField):

    def clean(self, value):
        super(char_field, self).clean(value)

        if value in ('',None):
            return None
        return value

class email_field(forms.EmailField):

    def clean(self, value):
        super(email_field, self).clean(value)

        if value in ('',None):
            return None
        return value

class software_field(object_name_field):

    def __init__(self, *args, **kwargs):
        super(software_field, self).__init__(models.software, *args, **kwargs)


class location_field(object_name_field):
    def __init__(self, *args, **kwargs):
        super(location_field, self).__init__(models.location, *args, **kwargs)


class license_field(forms.IntegerField):
    def clean(self, value):
        value=super(license_field, self).clean(value)

        if value in ('',None):
            return None

        try:
            license=models.license.objects.get(id=value)
        except models.license.DoesNotExist, e:
            raise ValidationError(u"Cannot find license %s: %s" % (value,e))

        return value

class party_field(select_field):
    def __init__(self, *args, **kwargs):
        super(party_field, self).__init__("party", *args, **kwargs)

class mac_address_field(forms.CharField):
    def clean(self, value):
        value=super(mac_address_field, self).clean(value)

        if value in ('',None):
            return None

        value = value.upper().strip()

        g = u"[A-F0-9][A-F0-9]";
        m = re.match(u"^(%s)-(%s)-(%s)-(%s)-(%s)-(%s)$"
                     %(g,g,g,g,g,g),value)
        if m != None:
                value = "%s:%s:%s:%s:%s:%s"%(m.group(1),m.group(2),m.group(3),m.group(4),m.group(5),m.group(6))

        m = re.match(u"^(%s):(%s):(%s):(%s):(%s):(%s)$"
                     %(g,g,g,g,g,g),value)
        if m == None:
            raise ValidationError(u"Invalid MAC address %s" % (value))

        return value

class hardware_field(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(hardware_field, self).__init__(*args, **kwargs)

    def clean(self, value):
        value=super(hardware_field, self).clean(value)

        if value in ('',None):
            return None

        parser = p.Keyword("computer") + p.Optional(p.Keyword("name")+p.Word(p.alphanums+"-_"))
        parser = parser | p.Keyword("user") + (p.QuotedString('"') | p.Word(p.alphanums))

        parser = p.Group(parser)
        parser = parser + p.ZeroOrMore(p.Keyword("and") + parser)

        parser = parser | p.Word(p.nums).setResultsName("pk")

        try:
            results = parser.parseString(value, parseAll=True)
        except p.ParseBaseException, e:
            raise ValidationError(u"Cannot parse '%s' loc: %s msg: %s"%(value, e.loc, e.msg))

        if results.pk != "":
            try:
                hardware=models.hardware.objects.get(pk=results.pk)
                return hardware.get_object()
            except models.party.DoesNotExist, e:
                raise forms.util.ValidationError(u"Cannot find hardware after applying '%s': %s" % (value,e))


        hardware=models.hardware.objects.all()
        count = hardware.count()

        while len(results) > 0:
            check = results.pop(0)

            if len(check) == 3 and check[0] == "computer" and check[1] == "name":
                hardware=hardware.filter(computer__name=check[2])
            elif check[0] == "computer":
                hardware=hardware.filter(computer__name__isnull=False)
            elif check[0] == "user":
                try:
                    party=models.party.objects.get(name = check[1])
                except models.party.DoesNotExist, e:
                    raise forms.util.ValidationError(u"Cannot find party for '%s': %s" % (check[1],e))
                hardware=hardware.filter(user=party)

            count = hardware.count()
            if count <= 0:
                raise forms.util.ValidationError(u"Cannot find hardware '%s'" % (check))

            if len(results) > 0:
                dummy = results.pop(0)

        if count > 1:
            raise forms.util.ValidationError(u"Too many results for '%s'"%(value))

        return hardware[0].get_object()
