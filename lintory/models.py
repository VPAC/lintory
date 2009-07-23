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

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode
from django.db import models
from django.template import loader

import lintory.eparty.fields as eparty
import lintory.mfields as fields

from datetime import *
import random
import re

# META INFORMATION FOR TYPES

class breadcrumb:
    def __init__(self,url,name):
        self.url = url
        self.name = name

class generic_type:
    def __init__(self,type_id):
        self.type_id = type_id

    def __unicode__(self):
        return self.single_name()

    def single_name(self):
        return self.type_id.replace("_"," ")

    def plural_name(self):
        return self.single_name() + 's'

    def has_add_perms(self,user):
        if user.is_authenticated() and user.has_perm('inventory.add_'+self.type_id):
            return True
        else:
            return False

    def has_edit_perms(self,user):
        if user.is_authenticated() and user.has_perm('inventory.edit_'+self.type_id):
            return True
        else:
            return False

    def has_delete_perms(self,user):
        if user.is_authenticated() and user.has_perm('inventory.delete_'+self.type_id):
            return True
        else:
            return False

    def get_breadcrumbs(self):
        breadcrumbs = []
        breadcrumbs.append(breadcrumb(reverse("lintory_root"),"home"))
        breadcrumbs.append(breadcrumb(reverse(self.type_id+"_list"),self.plural_name()))
        return breadcrumbs

    def get_create_breadcrumbs(self, **kwargs):
        breadcrumbs = self.get_breadcrumbs(**kwargs)
        breadcrumbs.append(breadcrumb(self.get_create_url(**kwargs),"create"))
        return breadcrumbs

    @models.permalink
    def get_create_url(self):
        return(self.type_id+"_create",)

types = {}

# BASE ABSTRACT MODEL CLASS

class model(models.Model):

    def get_type(self):
        type_id = type(self).__name__
        return types[type_id]

    type = property(get_type)

    class Meta:
        abstract = True

    def get_history(self):
        ct = ContentType.objects.get_for_model(self)
        return history_item.objects.filter(content_type=ct, object_pk=self.pk)

    def error_list(self):
        error_list = []
        return error_list

    # VIEW ACTION

    # get the URL to display this object
    # note this may not always make sense
    @models.permalink
    def get_absolute_url(self):
        return(self.type.type_id+'_detail', [ str(self.pk) ])

    # get the breadcrumbs to show while displaying this object
    def get_breadcrumbs(self):
        breadcrumbs = self.type.get_breadcrumbs()
        breadcrumbs.append(breadcrumb(self.get_absolute_url(),self))
        return breadcrumbs

    # CREATE ACTION

    # EDIT ACTION

    # get the URL to edit this object
    @models.permalink
    def get_edit_url(self):
        return(self.type.type_id+'_edit', [ str(self.pk) ])

    # get breadcrumbs to show while editing this object
    def get_edit_breadcrumbs(self):
        breadcrumbs = self.get_breadcrumbs()
        breadcrumbs.append(breadcrumb(self.get_edit_url(),"edit"))
        return breadcrumbs

    # find link we should go to after editing this object
    def get_edited_url(self):
        return self.get_absolute_url()

    # DELETE ACTION

    # get the URL to delete this object
    @models.permalink
    def get_delete_url(self):
        return(self.type.type_id+'_delete', [ str(self.pk) ])

    # get breadcrumbs to show while deleting this object
    def get_delete_breadcrumbs(self):
        breadcrumbs = self.get_breadcrumbs()
        breadcrumbs.append(breadcrumb(self.get_delete_url(),"delete"))
        return breadcrumbs

    # are there any reasons why this object should not be deleted?
    def check_delete(self):
        error_list = []
        return error_list

    # find link we should go to after deleting object
    @models.permalink
    def get_deleted_url(self):
        return(self.type.type_id+"_list",)


# PARTY CLASSES

class Nobody:

    def get_breadcrumbs(self):
        breadcrumbs = self.type.get_breadcrumbs()
        breadcrumbs.append(breadcrumb(reverse("party_detail",args=("none",)),"Nobody"))
        return breadcrumbs

    def __unicode__(self):
        return "Nobody"

    def __init__(self):
        self.type = types["party"]
        self.pk = "none"
        self.assigned_hardware_tasks = hardware_task.objects.filter(assigned__isnull=True,
                date_complete__isnull=True)
        self.owns_locations = location.objects.filter(owner__isnull=True)
        self.uses_locations = location.objects.filter(user__isnull=True)
        self.owns_licenses = license.objects.filter(owner__isnull=True)
        self.owns_hardware = hardware.objects.filter(owner__isnull=True,
                date_of_disposal__isnull=True)
        self.uses_hardware = hardware.objects.filter(user__isnull=True,
                date_of_disposal__isnull=True)
        self.owns_software = software.objects.filter(
                license_key__isnull = False,
                license_key__license__owner__isnull = True).distinct()

    def error_list(self):
        error_list = []
        return error_list

class party(model):
    name     = fields.char_field(max_length=30)
    eparty   = eparty.name_model_field(null=True,blank=True,db_index=True)
    comments = fields.text_field(null=True, blank=True)

    def owns_software(self):
        return software.objects.filter(license_key__license__owner = self).distinct()

    def __unicode__(self):
        return self.name

    def error_list(self):
        error_list = super(party,self).error_list()
        if isinstance(self.eparty,eparty.Error_Name):
            error_list.append("E-Party entry does not exist")
        return error_list

class party_type(generic_type):
    def plural_name(self):
        return "parties"

types['party'] = party_type('party')

# MODEL CLASSES

class history_item(model):
    # Content-object field
    content_type   = models.ForeignKey(ContentType,
            related_name="content_type_set_for_%(class)s")
    object_pk      = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    date  = models.DateTimeField()
    title = fields.char_field(max_length=80)
    body  = fields.text_field(null=True,blank=True)

    def __unicode__(self):
        return u"history item %s"%(self.title)

    def get_breadcrumbs(self):
        breadcrumbs = types['history_item'].get_breadcrumbs(self.content_object)
        return breadcrumbs

    def get_edit_breadcrumbs(self):
        breadcrumbs = self.get_breadcrumbs()
        breadcrumbs.append(breadcrumb(self.get_edit_url(),"edit history"))
        return breadcrumbs

    def get_delete_breadcrumbs(self):
        breadcrumbs = self.get_breadcrumbs()
        breadcrumbs.append(breadcrumb(self.get_delete_url(),"delete history"))
        return breadcrumbs

    @models.permalink
    def get_edit_url(self):
        return('history_item_edit', [ str(self.pk) ])

    @models.permalink
    def get_delete_url(self):
        return('history_item_delete', [ str(self.pk) ])

    def get_edited_url(self):
        return self.content_object.get_absolute_url()

    def get_deleted_url(self):
        return self.content_object.get_absolute_url()

class history_item_type(generic_type):

    def get_breadcrumbs(self, object):
        breadcrumbs = object.get_breadcrumbs()
        return breadcrumbs

    @models.permalink
    def get_create_url(self, object):
        return(self.type_id+"_create", [ object.type.type_id, object.pk ] )

    def get_create_breadcrumbs(self, **kwargs):
        breadcrumbs = self.get_breadcrumbs(**kwargs)
        breadcrumbs.append(breadcrumb(self.get_create_url(**kwargs),"create history"))
        return breadcrumbs

types['history_item'] = history_item_type('history_item')

class vendor(model):
    name     = fields.char_field(max_length=30)
    address  = fields.text_field(null=True, blank=True)
    telephone = fields.char_field(max_length=20, null=True, blank=True)
    email    = fields.email_field(null=True, blank=True)
    comments = fields.text_field(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def check_delete(self):
        errorlist = []

        if self.software_set.all().count() > 0:
            errorlist.append("Cannot delete vendor with software")
        if self.hardware_set.all().count() > 0:
            errorlist.append("Cannot delete vendor with hardware")
        if self.license_set.all().count() > 0:
            errorlist.append("Cannot delete vendor with licenses")
        if self.computer_set.all().count() > 0:
            errorlist.append("Cannot delete vendor with computers")

        return errorlist

types['vendor'] = generic_type('vendor')

class location(model):
    name    = fields.char_field(max_length=30)
    address = fields.text_field(null=True,blank=True)
    old_owner   = eparty.name_model_field(null=True,blank=True,db_index=True)
    old_user    = eparty.name_model_field(null=True,blank=True,db_index=True)
    owner   = models.ForeignKey(party,null=True,blank=True, related_name='owns_locations')
    user    = models.ForeignKey(party,null=True,blank=True, related_name='uses_locations')
    parent  = models.ForeignKey('self',related_name='children',null=True,blank=True)

    comments = fields.text_field(null=True,blank=True)

    @models.permalink
    def get_create_url(self):
        return('location_create', [ str(self.pk) ])

    def get_absolute_svg_url(self):
        try:
            t = loader.get_template('lintory/locations/%i.svg' % self.id)
            return reverse('location_svg', args=[ str(self.pk) ])
        except loader.TemplateDoesNotExist:
            return None

    def get_breadcrumbs(self):
        breadcrumbs = []
        breadcrumbs.append(breadcrumb(reverse("lintory_root"),"home"))

        object=self
        seen = {}
        while object is not None and object.pk not in seen:
            breadcrumbs.insert(1,breadcrumb(object.get_absolute_url(),object))
            seen[object.pk] = True
            object = object.parent

        if object is not None:
            breadcrumbs.insert(1,breadcrumb(object.get_absolute_url(),"ERROR"))

        return breadcrumbs

    def get_deleted_url(self):
        if self.parent is not None:
                return self.parent.get_absolute_url()
        else:
                return reverse("lintory_root")

    def __unicode__(self):
        return self.name

    def _get_self_or_children(self, seen):
        if self.pk in seen:
            return []

        seen[self.pk] = True
        list = [ self ]
        children = location.objects.filter(parent=self)
        for child in children:
                list.extend(child._get_self_or_children(seen))

        return list

    def get_self_or_children(self):
        seen = {}
        return self._get_self_or_children(seen)

    def get_hardware(self):
        return self.hardware_set.filter(date_of_disposal__isnull=True);

    def get_self_or_children_hardware(self):
        children = self.get_self_or_children();
        return hardware.objects.filter(location__in=children,date_of_disposal__isnull=True);

    def get_owner(self):
        return self.owner

    def get_user(self):
        return self.user

    class Meta:
        ordering = ('name',)

    def check_delete(self):
        errorlist = []
        return errorlist

    def tasks(self):
        hardware = self.get_self_or_children_hardware()
        return task.objects.filter(hardware_task__hardware__in=hardware,hardware_task__date_complete__isnull=True).distinct()

    def error_list(self):
        error_list = super(location,self).error_list()

        if self.owner is None:
            error_list.append("Owner not defined")

        if self.user is None:
            error_list.append("User not defined")

        return error_list

class location_type(generic_type):

    def get_breadcrumbs(self, parent):
        breadcrumbs = parent.get_breadcrumbs()
        return breadcrumbs

    @models.permalink
    def get_create_url(self, parent):
        return(self.type_id+"_create", [ parent.pk ] )

types['location'] = location_type('location')

class hardware(model):
    type_id       = fields.char_field(max_length=20)
    seen_first    = models.DateTimeField()
    seen_last     = models.DateTimeField()
    manufacturer  = fields.char_field(max_length=50,null=True,blank=True)
    model         = fields.char_field(max_length=90,null=True,blank=True)
    product_number= fields.char_field(max_length=30,null=True,blank=True)
    serial_number = fields.char_field(max_length=50,null=True,blank=True)
    service_number= fields.char_field(max_length=10,null=True,blank=True)
    date_of_manufacture = models.DateTimeField(null=True,blank=True)
    date_of_disposal    = models.DateTimeField(null=True,blank=True)
    asset_id = fields.char_field(max_length=10,null=True,blank=True)
    old_owner    = eparty.name_model_field(null=True,blank=True,db_index=True)
    old_user     = eparty.name_model_field(null=True,blank=True,db_index=True)
    owner   = models.ForeignKey(party,null=True,blank=True, related_name='owns_hardware')
    user    = models.ForeignKey(party,null=True,blank=True, related_name='uses_hardware')
    location = models.ForeignKey(location,null=True,blank=True)
    vendor  = models.ForeignKey(vendor,null=True,blank=True)

    installed_on  = models.ForeignKey('self',related_name='installed_hardware',null=True,blank=True)
    auto_delete = models.BooleanField()
    auto_manufacturer = fields.char_field(max_length=50,null=True,blank=True,db_index=True)
    auto_model = fields.char_field(max_length=90,null=True,blank=True,db_index=True)
    auto_serial_number = fields.char_field(max_length=50,null=True,blank=True,db_index=True)

    comments = fields.text_field(null=True,blank=True)

    def get_type_id(self):
        if self.type_id is not None and self.type_id!="":
            type_id = self.type_id
        elif type(self) != hardware:
            type_id = type(self).__name__
        else:
            raise RuntimeError("Unknown type for generic hardware type")

        return type_id

    def get_type(self):
        type_id = self.get_type_id()
        return types[type_id]

    type = property(get_type)

    def __unicode__(self):
        return "%s - %s %s"%(self.type.single_name(),self.manufacturer,self.model)

    class Meta:
        ordering = ('type_id', 'manufacturer','model')

    @models.permalink
    def get_absolute_url(self):
        return('hardware_detail', [ str(self.pk) ])

    @models.permalink
    def get_edit_url(self):
        return('hardware_edit', [ str(self.pk) ])

    @models.permalink
    def get_delete_url(self):
        return('hardware_delete', [ str(self.pk) ])

    def get_owner(self):
        return self.owner

    def get_user(self):
        return self.user

    def get_object(self):
        # No need to get type data if we we already that type
        if type(self) != hardware:
            return self

        # Get type data by our type
        if self.type_id == "computer":
            return self.computer
        elif self.type_id == "storage":
            return self.storage
        elif self.type_id == "monitor":
            return self.monitor
        elif self.type_id == "network_adaptor":
            return self.network_adaptor
        else:
            raise RuntimeError("Unknown hardware type %s"%(self.type))

    def hardware_tasks_all(self):
        return self.hardware_task_set.all()

    def hardware_tasks_done(self):
        return self.hardware_task_set.filter(date_complete__isnull=False)

    def hardware_tasks_todo(self):
        return self.hardware_task_set.filter(date_complete__isnull=True)

    def check_delete(self):
        errorlist = []
        if self.installed_on != None:
            errorlist.append("Cannot delete hardware that is installed")
        return errorlist

    @models.permalink
    def get_deleted_url(self):
        return("hardware_type_list", [self.type_id])

    def save(self, *args,**kwargs):
        self.type_id = self.get_type_id()
        super(hardware,self).save(*args, **kwargs)
    save.alters_data = True

    def get_breadcrumbs(self):
        if type(self) == hardware:
            return self.get_object().get_breadcrumbs()
        else:
            return super(hardware,self).get_breadcrumbs()

    def error_list(self):
        error_list = super(hardware,self).error_list()
        if self.installed_on is not None:
            if self.location is not None:
                error_list.append("Location defined when hardware is installed")
            if self.user is not None:
                error_list.append("User defined when hardware is installed")
        else:
            if self.location is None:
                error_list.append("Location not defined")
            if self.owner is None:
                error_list.append("Owner not defined")
            if self.user is None:
                error_list.append("User not defined")

        return error_list

class hardware_base_type(generic_type):
    def plural_name(self):
        return "hardware"

types['hardware'] = hardware_base_type('hardware')

class hardware_type(generic_type):
    def get_breadcrumbs(self):
        breadcrumbs = types['hardware'].get_breadcrumbs()
        breadcrumbs.append(breadcrumb(reverse("hardware_type_list",args=[self.type_id]),self.plural_name()))
        return breadcrumbs

    @models.permalink
    def get_create_url(self):
        return("hardware_type_create", [ self.type_id ])


class storage(hardware):
    used_by  = models.ForeignKey('computer',related_name='used_storage',null=True,blank=True)
    total_size = models.DecimalField(max_digits=12,decimal_places=0,null=True,blank=True)
    sector_size = models.PositiveIntegerField(null=True,blank=True)

    def os_list(self):
        return self.os_set.all()

    def active_software_installations(self):
        os_list = self.os_list()
        return software_installation.objects.filter(active=True, os__in=os_list)

    def inactive_software_installations(self):
        os_list = self.os_list()
        return software_installation.objects.filter(active=False, os__in=os_list)

    def check_delete(self):
        errorlist = super(storage,self).check_delete()
        if self.installed_on != None:
            errorlist.append("Cannot delete storage that is in use on a computer")
        if self.os_set.all().count() > 0:
            errorlist.append("Cannot delete storage with OS")
        return errorlist

    def __unicode__(self):
        if self.total_size is None or self.sector_size is None:
            return u"harddisk"

        size = self.total_size*self.sector_size
        units = "bytes"

        if size > 1000:
            size = size / 1000
            units = "KB"

        if size > 1000:
            size = size / 1000
            units = "MB"

        if size > 1000:
            size = size / 1000
            units = "GB"

        if size > 1000:
            size = size / 1000
            units = "TB"

        return u"%d %s harddisk"%(size, units)

    def error_list(self):
        error_list = super(storage,self).error_list()
        if self.installed_on is not None:
            if self.used_by is None:
                error_list.append("Storage is installed but not marked in use")
            elif self.installed_on.pk != self.used_by.pk:
                # Not an error really, but just in case
                error_list.append("Storage is installed but in use by different machine")
        return error_list

class storage_type(hardware_type):
    def plural_name(self):
        return "storage"

types['storage'] = storage_type('storage')

class monitor(hardware):
    size = models.FloatField(null=True,blank=True)
    width = models.FloatField(null=True,blank=True)
    height = models.FloatField(null=True,blank=True)

    def __unicode__(self):
        if self.size is None:
            return "monitor"
        else:
            return "%s\" inch monitor"%(self.size)

types['monitor'] = hardware_type('monitor')

class computer(hardware):
    name = fields.char_field(max_length=20)
    is_portable = models.BooleanField()

    memory = models.DecimalField(max_digits=12,decimal_places=0,null=True,blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name','asset_id')

    def seen_first_delta(self):
        return datetime.now() - self.seen_first

    def seen_last_delta(self):
        return datetime.now() - self.seen_last

    def os_list(self):
        storage_list = self.used_storage.all()
        return os.objects.filter(storage__in=storage_list)

    def active_software_installations(self):
        os_list = self.os_list()
        return software_installation.objects.filter(active=True, os__in=os_list)

    def inactive_software_installations(self):
        os_list = self.os_list()
        return software_installation.objects.filter(active=False, os__in=os_list)

    def network_adaptors(self):
        return network_adaptor.objects.filter(installed_on=self)

    def check_delete(self):
        errorlist = super(computer,self).check_delete()
        if self.license_set.all().count() > 0:
            errorlist.append("Cannot delete computer with licenses")
        if self.installed_hardware.all().count() > 0:
            errorlist.append("Cannot delete computer with installed hardware")
        if self.used_storage.all().count() > 0:
            errorlist.append("Cannot delete computer with used storage")
        return errorlist

types['computer'] = hardware_type('computer')

class network_adaptor(hardware):
    name = fields.char_field(max_length=100)
    network_type = fields.char_field(max_length=20)
    mac_address = fields.mac_address_field(db_index=True)
    IPv4_address = models.IPAddressField(null=True,blank=True)

    def inet6_host_id(self):
        mac = self.mac_address.split(':')
        mac[3:3] = ['ff', 'fe']
        mac = [ int(i,16) for i in mac ]
        mac[0] = mac[0] | 2

        addr = []
        for i in range(0,4):
                addr.append(mac[i*2] << 8 | mac[i*2+1])

        return u"%x:%x:%x:%x"%(addr[0],addr[1],addr[2],addr[3])

    def __unicode__(self):
        return self.name

    def error_list(self):
        error_list = super(network_adaptor,self).error_list()

        g = u"[A-F0-9][A-F0-9]";
        m = re.match(u"^(%s):(%s):(%s):(%s):(%s):(%s)$"
                     %(g,g,g,g,g,g),self.mac_address)
        if m is None:
            error_list.append(u"Mac address %s not in required format"%(self.mac_address))

        duplicates = network_adaptor.objects.filter(mac_address=self.mac_address).exclude(pk=self.pk)
        if duplicates.count() > 0:
            error_list.append(u"Ethernet address %s is duplicated"%(self.mac_address))

        return error_list

class network_adaptor_type(hardware_type):
    pass

types['network_adaptor'] = network_adaptor_type('network_adaptor')

class os(model):
    storage = models.ForeignKey(storage)
    name = fields.char_field(max_length=40, db_index=True)
    computer_name = fields.char_field(max_length=20, db_index=True)
    seen_first    = models.DateTimeField()
    seen_last     = models.DateTimeField()

    comments = fields.text_field(null=True,blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('storage', 'name')

    def seen_first_delta(self):
        return datetime.now() - self.seen_first

    def seen_last_delta(self):
        return datetime.now() - self.seen_last

    def active_software_installations(self):
        return self.software_installation_set.filter(active=True)

    def inactive_software_installations(self):
        return self.software_installation_set.filter(active=False)

    def check_delete(self):
        errorlist = []
        return errorlist

    def get_breadcrumbs(self):
        breadcrumbs = self.type.get_breadcrumbs(storage=self.storage)
        breadcrumbs.append(breadcrumb(self.get_absolute_url(),self))
        return breadcrumbs

    def get_deleted_url(self):
        return self.storage.get_absolute_url()

class os_type(generic_type):
    def get_breadcrumbs(self, storage):
        breadcrumbs = storage.get_breadcrumbs()
        return breadcrumbs

    @models.permalink
    def get_create_url(self, storage):
        return(self.type_id+"_create", [ storage.pk ] )

    def single_name(self):
        return 'OS'

    def plural_name(self):
        return 'OSes'

types['os'] = os_type('os')

class software(model):
    name = fields.char_field(max_length=100)
    comments = fields.text_field(null=True,blank=True)
    vendor  = models.ForeignKey(vendor,null=True,blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)

    def licenses(self):
        return license.objects.filter(license_key__software=self).distinct()

    def software_installations_max(self):
        software_installations_max = None
        for l in self.licenses():
            m = l.installations_max
            if m is not None:
                if software_installations_max is None:
                    software_installations_max = m
                else:
                    software_installations_max += m
            else:
                return None
        return software_installations_max

    def software_installations_found(self):
        list = self.active_software_installations()
        return list.count()

    def software_installations_left(self):
        max = self.software_installations_max()
        if max is not None:
                return max - self.software_installations_found()
        else:
                return None

    def active_software_installations(self):
        return software_installation.objects.filter(software=self,active=True)

    def inactive_software_installations(self):
        return software_installation.objects.filter(software=self,active=False)

    @models.permalink
    def get_add_software_installation_url(self):
        return('software_add_software_installation', [ str(self.pk) ])

    @models.permalink
    def get_add_license_url(self):
        return('software_add_license', [ str(self.pk) ])

    def check_delete(self):
        errorlist = []
        if self.license_key_set.all().count() > 0:
            errorlist.append("Cannot delete software with license keys")
        if self.active_software_installations().count() > 0:
            errorlist.append("Cannot delete software with active installations")
        return errorlist

class software_type(generic_type):
    def plural_name(self):
        return "software"

types['software'] = software_type('software')

class license(model):
    name = fields.char_field(max_length=100,null=True,blank=True,db_index=True)
    vendor  = models.ForeignKey(vendor,null=True,blank=True)
    vendor_tag = fields.char_field(max_length=10,null=True,blank=True)
    installations_max = models.PositiveIntegerField(null=True,blank=True)
    version    = fields.char_field(max_length=20,null=True,blank=True)
    computer = models.ForeignKey(computer,null=True,blank=True)
    expires = models.DateTimeField(null=True,blank=True)
    old_owner    = eparty.name_model_field(null=True,blank=True,db_index=True)
    owner   = models.ForeignKey(party,null=True,blank=True, related_name='owns_licenses')
    text = fields.text_field(null=True,blank=True)
    comments = fields.text_field(null=True,blank=True)

    def __unicode__(self):
        if self.name is not None:
            name = self.name
        else:
            name = u"L%s"%(self.id)

        if self.vendor_tag is not None:
            name +=u" (%s)"%(self.vendor_tag)

        return name

    def software_installations_found(self):
        list = self.active_software_installations()
        return list.count()

    def software_installations_left(self):
        max=self.installations_max
        if max is None:
            return None
        else:
            return max - self.software_installations_found()

    def active_software_installations(self):
        return software_installation.objects.filter(active=True,license_key__license=self)

    def inactive_software_installations(self):
        return software_installation.objects.filter(active=False,license_key__license=self)

    @models.permalink
    def get_add_license_key_url(self):
        return('license_add_license_key', [ str(self.pk) ])

    def get_owner(self):
        return self.owner

    def error_list(self):
        error_list = super(license,self).error_list()

        if self.name is not None:
            duplicates = license.objects.filter(name=self.name).exclude(pk=self.pk)
            if duplicates.count() > 0:
                error_list.append(u"License name %s is duplicated"%(self.name))

        if self.owner is None:
            error_list.append("No owner defined")

        if self.license_key_set.count() == 0:
            error_list.append(u"no license keys defined for license")

        left = self.software_installations_left()
        if left is not None and left < 0:
            error_list.append(u"Negative installations left")

        for lk in self.license_key_set.all():
            error_list.extend(lk.error_list())

        return error_list

    def check_delete(self):
        errorlist = []
        if self.software_installations_found() > 0:
            errorlist.append("Cannot delete license with installations")
        return errorlist

types['license'] = generic_type('license')

class license_key(model):
    software = models.ForeignKey(software)
    license  = models.ForeignKey(license)
    key = fields.char_field(max_length=50,null=True,blank=True,db_index=True)
    comments = fields.text_field(null=True,blank=True)

    class Meta:
        ordering = ('software','license','key')
        permissions = (
            ("can_see_key", "Can see license key"),
        )


    def __unicode__(self):
        if self.key is not None:
                return self.key
        else:
                return "N/A"

    def active_software_installations(self):
        return software_installation.objects.filter(active=True,license_key=self)

    def inactive_software_installations(self):
        return software_installation.objects.filter(active=False,license_key=self)

    def software_installations_found(self):
        list = self.active_software_installations()
        return list.count()

    def error_list(self):
        error_list = super(license_key,self).error_list()

        duplicates = license_key.objects.filter(
                models.Q(software=self.software,key=self.key) |
                models.Q(software=self.license,key=self.key)
                ).exclude(pk=self.pk)
        if duplicates.count() > 0:
            error_list.append(u"License key %s is duplicated"%(self.key))

        return error_list

    def check_delete(self):
        errorlist = []
        if object.software_installations_found() > 0:
            errorlist.append("Cannot delete license key with installations")
        return errorlist

    def get_breadcrumbs(self):
        breadcrumbs = self.software.get_breadcrumbs()
        breadcrumbs.append(breadcrumb(self.get_absolute_url(),self))
        return breadcrumbs

    def get_deleted_url(self):
        return self.software.get_absolute_url()

class license_key_type(generic_type):
    def get_breadcrumbs(self, license):
        breadcrumbs = license.get_breadcrumbs()
        return breadcrumbs

    @models.permalink
    def get_create_url(self, license):
        return("license_add_"+self.type_id, [ license.pk ] )

types['license_key'] = license_key_type('license_key')

class software_installation(model):
    os = models.ForeignKey(os)
    software = models.ForeignKey(software)
    active = models.BooleanField()
    seen_first = models.DateTimeField()
    seen_last  = models.DateTimeField()

    license_key = models.ForeignKey(license_key,null=True,blank=True)

    software_version = fields.char_field(max_length=20,null=True,blank=True)

    auto_license_key = fields.char_field(max_length=50,null=True,blank=True)
    auto_delete = models.BooleanField()

    comments = fields.text_field(null=True,blank=True)

    def seen_first_delta(self):
        return datetime.now() - self.seen_first

    def seen_last_delta(self):
        return datetime.now() - self.seen_last

    class Meta:
        ordering = ('os','software','license_key')

    def error_list(self):
        error_list = super(software_installation,self).error_list()

        if self.license_key != None:
            if self.software != self.license_key.software:
                error_list.append(u"software %s does not match license key software %s"%(self.software,self.license_key.software))

            license=self.license_key.license;

            versions_allowed=license.version
            if versions_allowed is not None and versions_allowed!="":
                if self.software_version is None:
                    test_version = ""
                else:
                    test_version = self.software_version
                if not re.match(versions_allowed,test_version):
                    error_list.append(u"version %s is not allowed by license"%(self.software_version))

            if license.computer is not None:
                computer = self.os.storage.used_by
                if computer is not None:
                    if computer.pk != license.computer.pk:
                        error_list.append(u"installation on %s is not allowed by license"%(computer))

            if license.expires is not None and license.expires < datetime.now():
                error_list.append(u"license has expired")

        elif self.software.license_key_set.count() > 0:
                error_list.append(u"no license key set for software software installation")

        return error_list

    @models.permalink
    def get_edit_license_key_url(self):
        return('software_installation_edit_license_key', [ str(self.pk) ])

    def get_edited_url(self):
        return self.software.get_absolute_url()

    def get_deleted_url(self):
        return self.software.get_absolute_url()

    def __unicode__(self):
        return self.software.name+"@"+self.os.name

    def check_delete(self):
        errorlist = []
        if object.active:
            errorlist.append("Cannot delete active software installation")
        return errorlist

    def get_breadcrumbs(self):
        breadcrumbs = self.software.get_breadcrumbs()
        return breadcrumbs

    def get_edit_breadcrumbs(self):
        breadcrumbs = self.get_breadcrumbs()
        breadcrumbs.append(breadcrumb(self.get_edit_url(),"edit installation"))
        return breadcrumbs

    def get_delete_breadcrumbs(self):
        breadcrumbs = self.get_breadcrumbs()
        breadcrumbs.append(breadcrumb(self.get_delete_url(),"delete installation"))
        return breadcrumbs

class software_installation_type(generic_type):
    def get_breadcrumbs(self, software):
        breadcrumbs = software.get_breadcrumbs()
        return breadcrumbs

    @models.permalink
    def get_create_url(self, software):
        return("software_add_"+self.type_id, [ software.pk ] )

    def get_create_breadcrumbs(self, **kwargs):
        breadcrumbs = self.get_breadcrumbs(**kwargs)
        breadcrumbs.append(breadcrumb(self.get_create_url(**kwargs),"create installation"))
        return breadcrumbs

types['software_installation'] = software_installation_type('software_installation')

class task(model):
    name = fields.char_field(max_length=40)

    comments = fields.text_field(null=True,blank=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_add_computer_url(self):
        return('task_add_computer', [ str(self.pk) ])

    def hardware_tasks_all(self):
        return self.hardware_task_set.all()

    def hardware_tasks_done(self):
        return self.hardware_task_set.filter(date_complete__isnull=False)

    def hardware_tasks_todo(self):
        return self.hardware_task_set.filter(date_complete__isnull=True)

    def check_delete(self):
        errorlist = []

        if self.hardware_task_set.all().count() > 0:
            errorlist.append("Cannot delete task with computers")

        return errorlist

types['task'] = generic_type('task')

class hardware_task(model):
    task = models.ForeignKey(task)
    hardware = models.ForeignKey(hardware)

    date_complete = models.DateTimeField(null=True,blank=True)
    old_assigned      = eparty.name_model_field(null=True,blank=True,db_index=True)
    assigned   = models.ForeignKey(party,null=True,blank=True, related_name='assigned_hardware_tasks')

    comments = fields.text_field(null=True,blank=True)

    def __unicode__(self):
        return "task %s on hardware %s"%(self.task,self.hardware.get_object())

    def get_breadcrumbs(self):
        breadcrumbs = self.task.get_breadcrumbs()
        return breadcrumbs

    def get_edit_breadcrumbs(self):
        breadcrumbs = self.get_breadcrumbs()
        breadcrumbs.append(breadcrumb(self.get_edit_url(),"edit hardware todo"))
        return breadcrumbs

    def get_delete_breadcrumbs(self):
        breadcrumbs = self.get_breadcrumbs()
        breadcrumbs.append(breadcrumb(self.get_delete_url(),"delete hardware todo"))
        return breadcrumbs

    def get_deleted_url(self):
        return self.task.get_absolute_url()

    def get_assigned(self):
        return self.assigned

    def check_delete(self):
        errorlist = []
        return errorlist

types['hardware_task'] = generic_type('hardware_task')

data_fs = FileSystemStorage(location=settings.UPLOAD_DIR)

def data_upload_to(instance, filename):
    dt = instance.datetime
    if dt is None:
        dt = datetime.now()

    name = "%s_%04d.txt"%(
            dt.strftime("%Y/%m/%d/%H_%M_%S"),
            random.randint(0, 9999)
    )
    return name

class data(model):
    datetime = models.DateTimeField(db_index=True)
    file = models.FileField(upload_to=data_upload_to,storage=data_fs)
    format = fields.char_field(max_length=10)
    computer = models.ForeignKey(computer,null=True,blank=True)
    create_computer = models.BooleanField()
    os = models.ForeignKey(os,null=True,blank=True)
    create_os = models.BooleanField()
    imported = models.DateTimeField(null=True,blank=True)
    last_attempt = models.DateTimeField(null=True,blank=True)
    errors = fields.text_field(null=True, blank=True)
    comments = fields.text_field(null=True, blank=True)

    class Meta:
        ordering = ('datetime','computer',)

types['data'] = generic_type('data')
