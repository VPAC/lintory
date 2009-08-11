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

from lintory import models
import django_tables as tables

from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

def edit_link(user, object):
    if object.type.has_edit_perms(user):
        return mark_safe("<a class='changelink' href='%s'>%s</a>"%(
                object.get_edit_url(),
                "edit"))
    else:
        return "-"

def edit_license_key_link(user, object):
    if object.type.has_edit_perms(user):
        return mark_safe("<a class='changelink' href='%s'>%s</a>"%(
                object.get_edit_license_key_url(),
                "key"))
    else:
        return "-"

def delete_link(user, object):
    if object.type.has_edit_perms(user):
        return mark_safe("<a class='deletelink' href='%s'>%s</a>"%(
                object.get_delete_url(),
                "delete"))
    else:
        return "-"

class action_table(tables.ModelTable):
    def __init__(self, user, type, *args, **kwargs):
        super(action_table,self).__init__(*args, **kwargs)
        if type.has_edit_perms(user):
            self.base_columns["edit"] = tables.Column(data=lambda row: edit_link(user, row.data),sortable=False)
        if type.has_delete_perms(user):
            self.base_columns["delete"] = tables.Column(data=lambda row: delete_link(user, row.data),sortable=False)

def resolve_field(object, name):
    # try to resolve relationships spanning attributes
    bits = name.split('__')
    current = object
    for bit in bits:
        # note the difference between the attribute being None and not
        # existing at all; assume "value doesn't exist" in the former
        # (e.g. a relationship has no value), raise error in the latter.
        # a more proper solution perhaps would look at the model meta
        # data instead to find out whether a relationship is valid; see
        # also ``_validate_column_name``, where such a mechanism is
        # already implemented).
        if not hasattr(current, bit):
            raise ValueError("Could not resolve %s from %s" % (bit, name))

        current = getattr(current, bit)
        if callable(current):
            current = current()
        # important that we break in None case, or a relationship
        # spanning across a null-key will raise an exception in the
        # next iteration, instead of defaulting.
        if current is None:
            break

    return current

def link_field(row, data=None, label=None):
    if data is None:
        current = row.data
    else:
        current = resolve_field(row.data, data)

    if label is None:
        label = current
    else:
        label = resolve_field(row.data, label)

    if current is not None:
        return mark_safe(u"<a href='%s'>%s</a>"%(current.get_absolute_url(),conditional_escape(label)))
    else:
        return mark_safe(u"-")

class party(action_table):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column(data=link_field)

    class Meta:
        model = models.party
        exclude = ('eparty', 'comments', )

class vendor(action_table):
    id = tables.Column(sortable=False, visible=False)
    telephone = tables.Column(sortable=False)
    email = tables.Column(sortable=False)
    name = tables.Column(data=link_field)

    class Meta:
        model = models.vendor
        exclude = ('url', 'address', 'comments', )

class location(action_table):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column(data=link_field)
    owner = tables.Column(data=lambda row: link_field(row, "owner"))
    user = tables.Column(data=lambda row: link_field(row, "user"))

    class Meta:
        model = models.location

        exclude = ('address', 'parent', 'comments', )

class hardware(action_table):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column(data=lambda row: link_field(row, "get_object"), sortable=False)
    type_id = tables.Column(name="Type")
    manufacturer = tables.Column()
    model = tables.Column()
    serial_number = tables.Column()
    asset_id = tables.Column()
    owner = tables.Column(data=lambda row: link_field(row, "owner"))
    user = tables.Column(data=lambda row: link_field(row, "user"))
    location = tables.Column(data=lambda row: link_field(row, "location"))
    installed_on = tables.Column(data=lambda row: link_field(row, "installed_on"))

    def __init__(self, user, type, *args, **kwargs):
        super(action_table,self).__init__(*args, **kwargs)
        if type.has_edit_perms(user):
            self.base_columns["edit"] = tables.Column(data=lambda row: edit_link(user, row.data.get_object()),sortable=False)
        if type.has_delete_perms(user):
            self.base_columns["delete"] = tables.Column(data=lambda row: delete_link(user, row.data.get_object()),sortable=False)

    class Meta:
        pass

def check_box(row,pks):
    checked = ""
    if row.data.pk in pks:
        checked = "checked='checked' "

    return mark_safe(
        "<input id='pk_%d' type='checkbox' name='pk' value='%d' %s/> <label for='pk_%d'>%s</label>"%(
            row.data.pk, row.data.pk, checked, row.data.pk, row.data))

class hardware_list_form(hardware):

    def __init__(self, pks, *args, **kwargs):
        super(hardware_list_form,self).__init__(*args, **kwargs)
        int_pks = {}
        for pk in pks:
            try:
                int_pks[int(pk)] = True
            except ValueError, e:
                # ignore illegal values
                pass

        self.base_columns["name"] = tables.Column(data=lambda row: check_box(row,int_pks),sortable=False)

        if 'edit' in self.base_columns:
            del self.base_columns["edit"]
        if 'delete' in self.base_columns:
            del self.base_columns["delete"]

    class Meta:
        pass

class os(action_table):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column(data=link_field)
    computer = tables.Column(data=lambda row: link_field(row, "storage__used_by"))
    storage = tables.Column(data=lambda row: link_field(row, "storage"))

    class Meta:
        model = models.os
        exclude = ( "seen_first", "seen_last", "comments", )

class software(action_table):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column(data=link_field)
    vendor = tables.Column(data=lambda row: link_field(row, "vendor"))
    max = tables.Column(data="software_installations_max", sortable=False)
    found = tables.Column(data="software_installations_found", sortable=False)
    left = tables.Column(data="software_installations_left", sortable=False)

    class Meta:
        model = models.software

class license(action_table):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column(data=link_field)
    vendor = tables.Column(data=lambda row: link_field(row, "vendor"))
    computer = tables.Column(data=lambda row: link_field(row, "computer"))
    expires = tables.Column()
    owner = tables.Column(data=lambda row: link_field(row, "owner"))
    max = tables.Column(data="installations_max", sortable=False)
    found = tables.Column(data="software_installations_found", sortable=False)
    left = tables.Column(data="software_installations_left", sortable=False)
    comments = tables.Column()

    class Meta:
        pass

class license_key(action_table):
    id = tables.Column(sortable=False, visible=False)
    key = tables.Column(data=link_field)
    software = tables.Column(data=lambda row: link_field(row, "software"))
    license = tables.Column(data=lambda row: link_field(row, "license"))
    comments = tables.Column()

    def __init__(self, user, type, *args, **kwargs):
        super(license_key,self).__init__(user, type, *args, **kwargs)
        if type.has_name_perms(user,"can_see_key"):
            self.base_columns['key'] = tables.Column(data=lambda row: link_field(row, None, "key"))

    class Meta:
        pass

class software_installation(action_table):
    id = tables.Column(sortable=False, visible=False)
    software = tables.Column(data=lambda row: link_field(row, "software"))
    software_version = tables.Column()
    computer = tables.Column(data=lambda row: link_field(row, "os__storage__used_by"))
    storage = tables.Column(data=lambda row: link_field(row, "os__storage"))
    os = tables.Column(data=lambda row: link_field(row, "os"))
    license_key = tables.Column(data=lambda row: link_field(row, "license_key"))
    comments = tables.Column()

    def __init__(self, user, type, *args, **kwargs):
        super(software_installation,self).__init__(user, type, *args, **kwargs)
        if type.has_edit_perms(user):
            self.base_columns["Key"] = tables.Column(data=lambda row: edit_license_key_link(user, row.data),sortable=False)
        if type.has_name_perms(user,"can_see_key"):
            self.base_columns['license_key'] = tables.Column(data=lambda row: link_field(row, "license_key", "license_key__key"))

    class Meta:
        pass

class task(action_table):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column(data=link_field)
    total = tables.Column(data=lambda row: row.data.hardware_tasks_all().count(),sortable=False)
    done = tables.Column(data=lambda row: row.data.hardware_tasks_done().count(),sortable=False)
    todo = tables.Column(data=lambda row: row.data.hardware_tasks_todo().count(),sortable=False)

    class Meta:
        model = models.task

class hardware_task(action_table):
    id = tables.Column(sortable=False, visible=False)
    task = tables.Column(data=lambda row: link_field(row, "task"))
    hardware = tables.Column(data=lambda row: link_field(row, "hardware"))
    assigned = tables.Column(data=lambda row: link_field(row, "assigned"))

    class Meta:
        model = models.hardware_task

class data(action_table):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column(data=link_field)
    datetime = tables.Column()
    format = tables.Column()
    computer = tables.Column(data=lambda row: link_field(row, "computer"))
    os = tables.Column(data=lambda row: link_field(row, "os"))
    imported = tables.Column()
    last_attempt = tables.Column()
    comments = tables.Column()

    class Meta:
        pass
