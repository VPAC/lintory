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

def link_row(row):
    return mark_safe(u"<a href='%s'>%s</a>"%(row.data.get_absolute_url(),conditional_escape(row.data)))

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

def link_field(row, name):
    current = resolve_field(row.data, name)

    if current is not None:
        return mark_safe(u"<a href='%s'>%s</a>"%(current.get_absolute_url(),conditional_escape(current)))
    else:
        return mark_safe(u"-")

class party(tables.ModelTable):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column(data=link_row)

    class Meta:
        model = models.party
        exclude = ('eparty', 'comments', )

class vendor(tables.ModelTable):
    id = tables.Column(sortable=False, visible=False)
    telephone = tables.Column(sortable=False)
    email = tables.Column(sortable=False)
    name = tables.Column(data=link_row)

    class Meta:
        model = models.vendor
        exclude = ('url', 'address', 'comments', )

class location(tables.ModelTable):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column(data=link_row)
    owner = tables.Column(data=lambda row: link_field(row, "owner"))
    user = tables.Column(data=lambda row: link_field(row, "user"))

    class Meta:
        model = models.location

        exclude = ('address', 'parent', 'comments', )

class hardware(tables.ModelTable):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column(data=link_row)
    type_id = tables.Column()
    manufacturer = tables.Column()
    model = tables.Column()
    serial_number = tables.Column()
    asset_id = tables.Column()
    owner = tables.Column(data=lambda row: link_field(row, "owner"))
    user = tables.Column(data=lambda row: link_field(row, "user"))
    location = tables.Column(data=lambda row: link_field(row, "location"))
    installed_on = tables.Column(data=lambda row: link_field(row, "installed_on"))

    class Meta:
        pass

class os(tables.ModelTable):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column(data=link_row)
    computer = tables.Column(data=lambda row: link_field(row, "storage__used_by"))
    storage = tables.Column(data=lambda row: link_field(row, "storage"))

    class Meta:
        model = models.os
        exclude = ( "seen_first", "seen_last", "comments", )

class software(tables.ModelTable):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column(data=link_row)
    vendor = tables.Column(data=lambda row: link_field(row, "vendor"))
    max = tables.Column(data="software_installations_max", sortable=False)
    found = tables.Column(data="software_installations_found", sortable=False)
    left = tables.Column(data="software_installations_left", sortable=False)

    class Meta:
        model = models.software

class license(tables.ModelTable):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column(data=link_row)
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

class license_key(tables.ModelTable):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column(data=link_row)
    software = tables.Column(data=lambda row: link_field(row, "software"))
    license = tables.Column(data=lambda row: link_field(row, "license"))
    comments = tables.Column()

    class Meta:
        pass

class software_installation(tables.ModelTable):
    id = tables.Column(sortable=False, visible=False)
    software = tables.Column(data=lambda row: link_field(row, "software"))
    computer = tables.Column(data=lambda row: link_field(row, "os__storage__used_by"))
    storage = tables.Column(data=lambda row: link_field(row, "os__storage"))
    os = tables.Column(data=lambda row: link_field(row, "os"))
    license_key = tables.Column(data=lambda row: link_field(row, "license_key"))
    comments = tables.Column()

    class Meta:
        pass

class task(tables.ModelTable):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column(data=link_row)
    total = tables.Column(data=lambda row: row.data.hardware_tasks_all().count(),sortable=False)
    done = tables.Column(data=lambda row: row.data.hardware_tasks_done().count(),sortable=False)
    todo = tables.Column(data=lambda row: row.data.hardware_tasks_todo().count(),sortable=False)

    class Meta:
        model = models.task

class hardware_task(tables.ModelTable):
    id = tables.Column(sortable=False, visible=False)
    task = tables.Column(data=lambda row: link_field(row, "task"))
    hardware = tables.Column(data=lambda row: link_field(row, "hardware"))
    assigned = tables.Column(data=lambda row: link_field(row, "assigned"))

    class Meta:
        model = models.hardware_task

class data(tables.ModelTable):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column(data=link_row)
    datetime = tables.Column()
    format = tables.Column()
    computer = tables.Column(data=lambda row: link_field(row, "computer"))
    os = tables.Column(data=lambda row: link_field(row, "os"))
    imported = tables.Column()
    last_attempt = tables.Column()
    comments = tables.Column()

    class Meta:
        pass
