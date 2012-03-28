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

from lintory import models, webs
import django_tables2 as tables

from django.http import QueryDict
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

def get_next_url(request):
    qd = QueryDict("",mutable=True)
    qd["next"] = request.get_full_path()
    return qd.urlencode()

class action_table(tables.Table):
    def __init__(self, request, web, *args, **kwargs):
        super(action_table,self).__init__(*args, **kwargs)
        self.request = request
        self.user = request.user
        self.web = web

        if web.has_edit_perms(self.user):
            self.base_columns["edit"] = tables.Column(sortable=False)
        if web.has_delete_perms(self.user):
            self.base_columns["delete"] = tables.Column(sortable=False)

    def render_edit(self, record):
        web = webs.get_web_from_object(record)
        return mark_safe("<a class='changelink' href='%s?%s'>%s</a>"%(
                web.get_edit_url(record),
                get_next_url(self.request),
                "edit"))

    def render_delete(self, record):
        web = webs.get_web_from_object(record)
        return mark_safe("<a class='deletelink' href='%s?%s'>%s</a>"%(
                web.get_delete_url(record),
                get_next_url(self.request),
                "delete"))

def render_link(record, title=None):
    if title is None:
        title=u"%s"%(record)

    if record is not None:
        web = webs.get_web_from_object(record)
        return mark_safe(u"<a href='%s'>%s</a>"%(
                web.get_view_url(record),
                conditional_escape(title)))
    else:
        return mark_safe(u"-")

class party(action_table):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column()

    def render_name(self, record):
        return render_link(record)

    class Meta:
        model = models.party
        exclude = ('eparty', 'comments', )

class vendor(action_table):
    id = tables.Column(sortable=False, visible=False)
    telephone = tables.Column(sortable=False)
    email = tables.Column(sortable=False)
    name = tables.Column()

    def render_name(self, record):
        return render_link(record)

    class Meta:
        model = models.vendor
        exclude = ('url', 'address', 'comments', )

class location(action_table):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column()
    owner = tables.Column()
    user = tables.Column()

    def render_name(self, record):
        return render_link(record)

    def render_owner(self, record):
        return render_link(record.owner)

    def render_user(self, record):
        return render_link(record.user)

    class Meta:
        model = models.location

        exclude = ('address', 'parent', 'comments', )

class hardware(action_table):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column(sortable=False)
    type_id = tables.Column(accessor="Type")
    manufacturer = tables.Column()
    model = tables.Column()
    serial_number = tables.Column()
    asset_id = tables.Column()
    owner = tables.Column()
    user = tables.Column()
    location = tables.Column()
    installed_on = tables.Column()

    def render_name(self, record):
        return render_link(record)

    def render_owner(self, record):
        return render_link(record.owner)

    def render_user(self, record):
        return render_link(record.user)

    def render_location(self, record):
        return render_link(record.location)

    def render_installed_on(self, record):
        return render_link(record.installed_on)

    def render_edit(self, record):
        return super(hardware, self).render_edit(record.get_object())

    def render_delete(self, record):
        return super(hardware, self).render_delete(record.get_object())

    class Meta:
        pass

class hardware_list_form(hardware):

    def __init__(self, pks, *args, **kwargs):
        super(hardware_list_form,self).__init__(*args, **kwargs)
        self.int_pks = {}
        for pk in pks:
            try:
                self.int_pks[int(pk)] = True
            except ValueError, e:
                # ignore illegal records
                pass

        self.base_columns["name"] = tables.Column(sortable=False)

        if 'edit' in self.base_columns:
            del self.base_columns["edit"]
        if 'delete' in self.base_columns:
            del self.base_columns["delete"]

    def render_name(self, record):
        checked = ""
        if record.pk in self.int_pks:
            checked = "checked='checked' "

        return mark_safe(
            "<input id='pk_%d' type='checkbox' name='pk' record='%d' %s/> <label for='pk_%d'>%s</label>"%(
                record.pk, record.pk, checked, record.pk, record))


    class Meta:
        pass

class os(action_table):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column()
    computer = tables.Column()
    storage = tables.Column()

    def render_name(self, record):
        return render_link(record)

    def render_computer(self, record):
        return render_link(record.storage.used_by)

    def render_storage(self, record):
        return render_link(record.storage)

    class Meta:
        model = models.os
        exclude = ( "seen_first", "seen_last", "comments", )

class software(action_table):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column()
    vendor = tables.Column()
    max = tables.Column(accessor="software_installations_max", sortable=False)
    found = tables.Column(accessor="software_installations_found", sortable=False)
    left = tables.Column(accessor="software_installations_left", sortable=False)

    def render_name(self, record):
        return render_link(record)

    def render_vendor(self, record):
        return render_link(record.vendor)

    class Meta:
        model = models.software

class license(action_table):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column()
    vendor = tables.Column()
    computer = tables.Column()
    expires = tables.Column()
    owner = tables.Column()
    max = tables.Column(accessor="installations_max", sortable=False)
    found = tables.Column(accessor="software_installations_found", sortable=False)
    left = tables.Column(accessor="software_installations_left", sortable=False)
    comments = tables.Column()

    def render_name(self, record):
        return render_link(record)

    def render_vendor(self, record):
        return render_link(record.vendor)

    def render_computer(self, record):
        return render_link(record.computer)

    def render_owner(self, record):
        return render_link(record.owner)

    class Meta:
        pass

class license_key(action_table):
    id = tables.Column(sortable=False, visible=False)
    key = tables.Column()
    software = tables.Column()
    license = tables.Column()
    comments = tables.Column()

    def render_key(self, record):
        return render_link(record)

    def render_software(self, record):
        return render_link(record.software)

    def render_license(self, record):
        return render_link(record.license)

    def render_key(self, record):
        if self.web.has_name_perms(self.user,"can_see_key"):
            return render_link(record, record.key)
        else:
            return render_link(record)

    class Meta:
        pass

class software_installation(action_table):
    id = tables.Column(sortable=False, visible=False)
    software = tables.Column()
    software_version = tables.Column()
    computer = tables.Column()
    storage = tables.Column()
    os = tables.Column()
    license_key = tables.Column()
    comments = tables.Column()

    def render_software(self, record):
        return render_link(record.software)

    def render_computer(self, record):
        return render_link(record.os.storage.used_by)

    def render_storage(self, record):
        return render_link(record.os.storage)

    def render_os(self, record):
        return render_link(record.os)

    def render_license_key(self, record):
        if record.license_key is None:
            return "-"
        elif self.web.has_name_perms(self.user,"can_see_key"):
            return render_link(record.license_key, record.license_key.key)
        else:
            return render_link(record.license_key)

    def __init__(self, request, web, *args, **kwargs):
        super(software_installation,self).__init__(request, web, *args, **kwargs)
        if web.has_edit_perms(request.user):
            self.base_columns["edit_key"] = tables.Column(sortable=False)

    def render_edit_key(self, record):
        web = webs.get_web_from_object(record)
        return mark_safe("<a class='changelink' href='%s?%s'>%s</a>"%(
                web.get_edit_license_key_url(record),
                get_next_url(self.request),
                "key"))

    class Meta:
        pass

class task(action_table):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column()
    total = tables.Column(sortable=False)
    done = tables.Column(sortable=False)
    todo = tables.Column(sortable=False)

    def render_name(self, record):
        return render_link(record)

    def render_total(self, record):
        return record.hardware_tasks_all().count()

    def render_done(self, record):
        return record.hardware_tasks_done().count()

    def render_todo(self, record):
        return record.hardware_tasks_todo().count()

    class Meta:
        model = models.task

class hardware_task(action_table):
    id = tables.Column(sortable=False, visible=False)
    task = tables.Column()
    hardware = tables.Column()
    user = tables.Column()
    assigned = tables.Column()

    def render_task(self, record):
        return render_link(record.task)

    def render_hardware(self, record):
        return render_link(record.hardware)

    def render_user(self, record):
        return render_link(record.hardware.user)

    def render_assigned(self, record):
        return render_link(record.assigned)

    class Meta:
        model = models.hardware_task

class data(action_table):
    id = tables.Column(sortable=False, visible=False)
    name = tables.Column()
    datetime = tables.Column()
    format = tables.Column()
    computer = tables.Column()
    os = tables.Column()
    imported = tables.Column()
    last_attempt = tables.Column()
    comments = tables.Column()

    def render_name(self, record):
        return render_link(record)

    def render_computer(self, record):
        return render_link(record.computer)

    def render_os(self, record):
        return render_link(record.os)

    class Meta:
        pass
