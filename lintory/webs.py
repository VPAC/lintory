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

import datetime

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models as m
from django.shortcuts import get_object_or_404
from django.forms import util
from django.utils.translation import ugettext as _

import django_webs

from lintory import models,forms

import os.path

################
# BASE METHODS #
################
class base_web(django_webs.web):
    app_label = "lintory"

get_web_from_object = django_webs.get_web_from_object
breadcrumb = django_webs.breadcrumb

#########
# PARTY #
#########

class party_web(base_web):
    web_id = "party"
    verbose_name_plural = "parties"
    model = models.party
    form = forms.party_form

    def get_view_buttons(self, user, instance):
        self.assert_instance_type(instance)
        buttons = super(party_web, self).get_view_buttons(user, instance)

        if self.has_view_perms(user):
            buttons.insert(0,{
                'class': 'viewlink',
                'text': 'Software',
                'url': self.get_software_list_url(instance),
            })

        return buttons

    @m.permalink
    def get_software_list_url(self, instance):
        self.assert_instance_type(instance)
        return('party_software_list', [ str(instance.pk) ])

    @m.permalink
    def get_software_view_url(self, instance, software):
        self.assert_instance_type(instance)
        return('party_software_detail', [ str(instance.pk), str(software.pk) ])

###########
# HISTORY #
###########

class history_item_web(base_web):
    web_id = "history_item"
    model = models.history_item
    form = forms.history_item_form

    def pre_save(self, instance, form):
        object = self.initial_object
        if object is not None:
            instance.content_type = ContentType.objects.get_for_model(object)
            instance.object_pk = object.pk
        return True

    def get_instance(self, object):
        instance = models.history_item()
        instance.date = datetime.datetime.now()
        return instance

    ###############
    # LIST ACTION #
    ###############

    ###############
    # VIEW ACTION #
    ###############

    def get_view_breadcrumbs(self, object):
        # note: object is the object containing history item, not the history item
        o_web = get_web_from_object(object.content_object)
        breadcrumbs = o_web.get_view_breadcrumbs(object.content_object)
        return breadcrumbs

    ##############
    # ADD ACTION #
    ##############

    @m.permalink
    def get_add_url(self, object):
        # note: object is the object containing history item, not the history item
        o_web = get_web_from_object(object)
        return("history_item_add", [ type(object).__name__, object.pk ] )

    def get_add_breadcrumbs(self, object):
        # note: object is the object containing history item, not the history item
        o_web = get_web_from_object(object)
        breadcrumbs = o_web.get_view_breadcrumbs(object)
        breadcrumbs.append(breadcrumb(self.get_add_url(object), "add history"))
        return breadcrumbs

    ###############
    # EDIT ACTION #
    ###############

    @m.permalink
    def get_edit_url(self, instance):
        self.assert_instance_type(instance)
        return('history_item_edit', [ str(instance.pk) ])

    def get_edit_finished_url(self, instance):
        self.assert_instance_type(instance)
        web = get_web_from_object(instance.content_object)
        return web.get_view_url(instance.content_object)

    # get breadcrumbs to show while editing this object
    def get_edit_breadcrumbs(self, instance):
        self.assert_instance_type(instance)
        breadcrumbs = self.get_view_breadcrumbs(instance)
        breadcrumbs.append(breadcrumb(self.get_edit_url(instance), "edit history"))
        return breadcrumbs

    #################
    # DELETE ACTION #
    #################

    @m.permalink
    def get_delete_url(self, instance):
        self.assert_instance_type(instance)
        return('history_item_delete', [ str(instance.pk) ])

    def get_delete_finished_url(self, instance):
        self.assert_instance_type(instance)
        web = get_web_from_object(instance.content_object)
        return web.get_view_url(instance.content_object)

    # get breadcrumbs to show while deleting this object
    def get_delete_breadcrumbs(self, instance):
        self.assert_instance_type(instance)
        breadcrumbs = self.get_view_breadcrumbs(instance)
        breadcrumbs.append(breadcrumb(self.get_delete_url(instance), "delete history"))
        return breadcrumbs



##########
# VENDOR #
##########

class vendor_web(base_web):
    web_id = "vendor"
    model = models.vendor
    form = forms.vendor_form

############
# LOCATION #
############

class location_web(base_web):
    web_id = "location"
    model = models.location
    form = forms.location_form

    def get_instance(self, parent):
        instance = models.location()
        instance.parent = parent
        return instance

    ###############
    # LIST ACTION #
    ###############

    ###############
    # VIEW ACTION #
    ###############

    def has_svg_file(self, instance):
        return os.path.exists("/etc/lintory/templates/lintory/locations/%i.svg"%instance.pk)

    @m.permalink
    def get_svg_url(self, instance):
        self.assert_instance_type(instance)
        return('location_svg', [ str(instance.pk) ])

    def get_view_breadcrumbs(self, instance):
        self.assert_instance_type(instance)

        breadcrumbs = []
        breadcrumbs.append(breadcrumb(reverse("root"), _("Home")))

        object=instance
        seen = {}
        while object is not None and object.pk not in seen:
            breadcrumbs.insert(1,breadcrumb(self.get_view_url(object),object))
            seen[object.pk] = True
            object = object.parent

        if object is not None:
            breadcrumbs.insert(1,breadcrumb(self.get_view_url(object), "ERROR"))

        return breadcrumbs

    def get_view_buttons(self, user, instance):
        self.assert_instance_type(instance)
        buttons = super(location_web, self).get_view_buttons(user, instance)

        if self.has_add_perms(user):
            buttons.insert(0,{
                'class': 'addlink',
                'text': 'Add location',
                'url': self.get_add_url(instance),
            })

        return buttons

    ##############
    # ADD ACTION #
    ##############

    @m.permalink
    def get_add_url(self, parent):
        return("location_add", [ parent.pk ] )

    def get_add_breadcrumbs(self, parent):
        breadcrumbs = self.get_view_breadcrumbs(parent)
        breadcrumbs.append(breadcrumb(self.get_add_url(parent), "add"))
        return breadcrumbs

    ###############
    # EDIT ACTION #
    ###############

    #################
    # DELETE ACTION #
    #################

    def get_delete_finished_url(self, instance):
        self.assert_instance_type(instance)
        if instance.parent is not None:
                return instance.parent.get_view_url()
        else:
                return reverse("root")

############
# HARDWARE #
############

hardware_types = {}

class hardware_metaclass(django_webs.web_metaclass):
    def __new__(cls, name, bases, attrs):
        result = django_webs.web_metaclass.__new__(cls, name, bases, attrs)
        if "web_id" in attrs:
            web_id = attrs["web_id"]
            hardware_types[web_id] = result
        return result

class hardware_web(base_web):
    __metaclass__ = hardware_metaclass
    web_id = "hardware"
    verbose_name_plural = "hardware"
    perm_prefix = "hardware"
    url_prefix = "hardware"
    model = models.hardware
    form = forms.hardware_form

    def assert_instance_type(self, instance):
        type_name = type(instance).__name__
        expected_type = self.web_id

        if expected_type == "hardware":
            if not type_name in hardware_types:
                raise RuntimeError("Expected a hardware type but got '%s'"%(type_name))
        else:
            if type_name != expected_type:
                raise RuntimeError("Expected type '%s' but got '%s'"%(expected_type,type_name))

    def get_breadcrumbs(self):
        breadcrumbs = []
        breadcrumbs.append(breadcrumb(reverse("root"), _("Home")))
        breadcrumbs.append(breadcrumb(reverse("hardware_list"), "hardware"))
        return breadcrumbs

    def get_instance(self):
        instance = self.initial_model_class()
        if self.initial_installed_on is not None:
            instance.installed_on = self.initial_installed_on
        instance.seen_first = datetime.datetime.now()
        instance.seen_last = datetime.datetime.now()
        return instance

    ###############
    # LIST ACTION #
    ###############

    ###############
    # VIEW ACTION #
    ###############

    def get_view_buttons(self, user, instance):
        self.assert_instance_type(instance)
        buttons = super(hardware_web, self).get_view_buttons(user, instance)

        if self.has_add_perms(user):
            buttons.insert(0,{
                'class': 'addlink',
                'text': 'Add hardware',
                'url': self.get_add_to_instance_url(instance),
            })

        if self.has_edit_perms(user):
            buttons.insert(1,{
                'class': 'changelink',
                'text': 'Install hardware',
                'url': self.get_install_url(instance),
            })

        return buttons

    ##############
    # ADD ACTION #
    ##############

    @m.permalink
    def get_add_url(self, type_id=None):
        if type_id==None:
            return("hardware_add",)
        else:
            return("hardware_type_add",[ type_id ])

    @m.permalink
    def get_add_to_instance_url(self, instance, type_id=None):
        self.assert_instance_type(instance)
        if type_id is None:
            return('hardware_add', [ str(instance.pk) ])
        else:
            return('hardware_add', [ str(instance.pk), str(type_id) ])

    ###############
    # EDIT ACTION #
    ###############

    @m.permalink
    def get_install_url(self, instance):
        self.assert_instance_type(instance)
        return('hardware_install', [ str(instance.pk) ])

    #################
    # DELETE ACTION #
    #################


class motherboard_web(hardware_web):
    web_id = "motherboard"
    model = models.motherboard
    form = forms.motherboard_form

class processor_web(hardware_web):
    web_id = "processor"
    model = models.processor
    form = forms.processor_form

class video_controller_web(hardware_web):
    web_id = "video_controller"
    model = models.video_controller
    form = forms.video_controller_form

class network_adaptor_web(hardware_web):
    web_id = "network_adaptor"
    model = models.network_adaptor
    form = forms.network_adaptor_form

class storage_web(hardware_web):
    web_id = "storage"
    verbose_name_plural = "storage"
    model = models.storage
    form = forms.storage_form

class power_supply_web(hardware_web):
    web_id = "power_supply"
    verbose_name_plural = "power supplies"
    model = models.power_supply
    form = forms.power_supply_form

class computer_web(hardware_web):
    web_id = "computer"
    model = models.computer
    form = forms.computer_form

class monitor_web(hardware_web):
    web_id = "monitor"
    model = models.monitor
    form = forms.monitor_form

class multifunction_web(hardware_web):
    web_id = "multifunction"
    model = models.multifunction
    form = forms.multifunction_form

class printer_web(hardware_web):
    web_id = "printer"
    model = models.printer
    form = forms.printer_form

class scanner_web(hardware_web):
    web_id = "scanner"
    model = models.scanner
    form = forms.scanner_form

class docking_station_web(hardware_web):
    web_id = "docking_station"
    model = models.docking_station
    form = forms.docking_station_form

class camera_web(hardware_web):
    web_id = "camera"
    model = models.camera
    form = forms.camera_form

######
# OS #
######

class os_web(base_web):
    web_id = "os"
    verbose_name_plural = "os"
    model = models.os
    form = forms.os_form

    ###############
    # LIST ACTION #
    ###############

    ###############
    # VIEW ACTION #
    ###############

    def get_view_breadcrumbs(self, instance):
        self.assert_instance_type(instance)
        web = storage_web()
        breadcrumbs = web.get_view_breadcrumbs(instance.storage)
        breadcrumbs.append(breadcrumb(self.get_view_url(instance), instance))
        return breadcrumbs

    ##############
    # ADD ACTION #
    ##############

    ###############
    # EDIT ACTION #
    ###############

    #################
    # DELETE ACTION #
    #################

    def get_delete_finished_url(self, instance):
        self.assert_instance_type(instance)
        web = storage_web()
        return web.get_view_url(instance.storage)

############
# SOFTWARE #
############
class software_web(base_web):
    web_id = "software"
    verbose_name_plural = "software"
    model = models.software
    form = forms.software_form

    ###############
    # LIST ACTION #
    ###############

    ###############
    # VIEW ACTION #
    ###############

    def get_view_buttons(self, user, instance):
        self.assert_instance_type(instance)
        buttons = super(software_web, self).get_view_buttons(user, instance)

        if self.has_add_license_perms(user):
            buttons.append({
                'class': 'addlink',
                'text': 'Add license',
                'url': self.get_add_license_url(instance),
            })

        if self.has_add_software_installation_perms(user):
            buttons.append({
                'class': 'addlink',
                'text': 'Add installation',
                'url': self.get_add_software_installation_url(instance),
            })

        return buttons

    ##############
    # ADD ACTION #
    ##############

    def has_add_software_installation_perms(self, user):
        web = software_installation_web()
        return web.has_add_perms(user)

    def has_add_license_perms(self, user):
        web = license_web()
        return web.has_add_perms(user)

    @m.permalink
    def get_add_software_installation_url(self, instance):
        self.assert_instance_type(instance)
        return('software_add_software_installation', [ str(instance.pk) ])

    @m.permalink
    def get_add_license_url(self, instance):
        self.assert_instance_type(instance)
        return('software_add_license', [ str(instance.pk) ])

    ###############
    # EDIT ACTION #
    ###############

    #################
    # DELETE ACTION #
    #################

###########
# LICENSE #
###########

class license_web(base_web):
    web_id = "license"
    model = models.license
    form = forms.license_form

    ###############
    # LIST ACTION #
    ###############

    ###############
    # VIEW ACTION #
    ###############

    def get_view_buttons(self, user, instance):
        self.assert_instance_type(instance)
        buttons = super(license_web, self).get_view_buttons(user, instance)

        if self.has_add_license_key_perms(user):
            buttons.append({
                'class': 'addlink',
                'text': 'Add key',
                'url': self.get_add_license_key_url(instance),
            })

        return buttons

    ##############
    # ADD ACTION #
    ##############

    def has_add_license_key_perms(self, user):
        web = license_web()
        return web.has_add_perms(user)

    @m.permalink
    def get_add_license_key_url(self, instance):
        self.assert_instance_type(instance)
        return('license_add_license_key', [ str(instance.pk) ])

    ###############
    # EDIT ACTION #
    ###############

    #################
    # DELETE ACTION #
    #################

###############
# LICENSE KEY #
###############

class license_key_web(base_web):
    web_id = "license_key"
    model = models.license_key
    form = forms.license_key_form

    def get_instance(self, license):
        instance = models.license_key()
        instance.license = license
        return instance

    ###############
    # LIST ACTION #
    ###############

    ###############
    # VIEW ACTION #
    ###############

    def get_view_breadcrumbs(self, instance):
        self.assert_instance_type(instance)
        web = license_web()
        breadcrumbs = web.get_view_breadcrumbs(instance.license)
        breadcrumbs.append(breadcrumb(web.get_view_url(instance.license), instance))
        return breadcrumbs

    ##############
    # ADD ACTION #
    ##############

    @m.permalink
    def get_add_url(self, license):
        return("license_add_license_key", [ license.pk ] )

    def get_add_breadcrumbs(self, license):
        web = license_web()
        breadcrumbs = web.get_view_breadcrumbs(license)
        breadcrumbs.append(breadcrumb(self.get_add_url(license), "add license key"))
        return breadcrumbs

    ###############
    # EDIT ACTION #
    ###############

    #################
    # DELETE ACTION #
    #################

    def get_delete_finished_url(self, instance):
        self.assert_instance_type(instance)
        software_web = software_web()
        return software_web.get_view_url(instance.software)


#########################
# SOFTWARE_INSTALLATION #
#########################

class software_installation_web(base_web):
    web_id = "software_installation"
    model = models.software_installation
    form = forms.software_installation_form

    def get_instance(self, software):
        instance = models.software_installation()
        instance.active = True
        instance.seen_first = datetime.datetime.now()
        instance.seen_last = datetime.datetime.now()
        instance.software = software
        return instance

    def pre_save(self, instance, form):
        valid = True
        if instance.license_key is not None:
            if instance.license_key.software != instance.software:
                msg = u"Software must match license key %s"%(instance.license_key.software)
                form._errors["software"] = util.ErrorList([msg])
                valid = False
        return valid

    ###############
    # LIST ACTION #
    ###############

    ###############
    # VIEW ACTION #
    ###############

    def get_view_breadcrumbs(self, instance):
        self.assert_instance_type(instance)
        web = get_web_for_object(instance.software)
        breadcrumbs = web.get_breadcrumbs(instance.software)
        breadcrumbs.append(breadcrumb(web.get_view_url(instance.software), instance))
        return breadcrumbs

    ##############
    # ADD ACTION #
    ##############

    @m.permalink
    def get_add_url(self, software):
        return("software_add_software_installation", [ software.pk ] )

    def get_add_breadcrumbs(self, software):
        web = software_web()
        breadcrumbs = web.get_view_breadcrumbs(software)
        breadcrumbs.append(breadcrumb(self.get_add_url(software), "add installation"))
        return breadcrumbs

    ###############
    # EDIT ACTION #
    ###############

    @m.permalink
    def get_edit_license_key_url(self, instance):
        self.assert_instance_type(instance)
        return('software_installation_edit_license_key', [ str(instance.pk) ])

    def get_edit_finished_url(self, instance):
        self.assert_instance_type(instance)
        web = software_web()
        return web.get_view_url(instance.software)

    def get_edit_breadcrumbs(self, instance):
        self.assert_instance_type(instance)
        web = software_web()
        breadcrumbs = web.get_view_breadcrumbs(instance.software)
        breadcrumbs.append(breadcrumb(self.get_edit_url(instance), "edit installation"))
        return breadcrumbs


    #################
    # DELETE ACTION #
    #################

    def get_delete_finished_url(self, instance):
        self.assert_instance_type(instance)
        return instance.software.get_view_url()

    def get_delete_breadcrumbs(self, instance):
        self.assert_instance_type(instance)
        breadcrumbs = instance.get_breadcrumbs()
        breadcrumbs.append(breadcrumb(instance.get_delete_url(), "delete installation"))
        return breadcrumbs


########
# TASK #
########

class task_web(base_web):
    web_id = "task"
    model = models.task
    form = forms.task_form

    ###############
    # LIST ACTION #
    ###############

    ###############
    # VIEW ACTION #
    ###############

    def get_view_buttons(self, user, instance):
        self.assert_instance_type(instance)
        buttons = super(task_web, self).get_view_buttons(user, instance)

        if self.has_add_hardware_perms(user):
            buttons.insert(0,{
                'class': 'addlink',
                'text': 'Add hardware',
                'url': self.get_add_hardware_url(instance),
            })

        return buttons

    ##############
    # ADD ACTION #
    ##############

    ###############
    # EDIT ACTION #
    ###############

    @m.permalink
    def get_add_hardware_url(self, instance):
        self.assert_instance_type(instance)
        return('task_add_hardware', [ str(instance.pk) ])

    def has_add_hardware_perms(self, user):
        web = hardware_task_web()
        return web.has_add_perms(user)

    #################
    # DELETE ACTION #
    #################


#################
# HARDWARE_TASK #
#################

class hardware_task_web(base_web):
    web_id = "hardware_task"
    model = models.hardware_task
    form = forms.hardware_task_form

    def get_instance(self, task):
        instance = models.hardware_task()
        instance.task = task
        return instance

    ###############
    # LIST ACTION #
    ###############

    ###############
    # VIEW ACTION #
    ###############

    def get_view_breadcrumbs(self, instance):
        self.assert_instance_type(instance)
        web = get_web_for_object(instance.task)
        breadcrumbs = web.get_breadcrumbs(instance.task)
        breadcrumbs.append(breadcrumb(web.get_view_url(instance.task), instance))
        return breadcrumbs

    ##############
    # ADD ACTION #
    ##############

    @m.permalink
    def get_add_url(self, task):
        return("task_add_hardware", [ task.pk ] )

    def get_add_breadcrumbs(self, task):
        web = task_web()
        breadcrumbs = web.get_view_breadcrumbs(task)
        breadcrumbs.append(breadcrumb(self.get_add_url(task), "add hardware"))
        return breadcrumbs

    ###############
    # EDIT ACTION #
    ###############

    def get_edit_breadcrumbs(self, instance):
        self.assert_instance_type(instance)
        web = task_web()
        breadcrumbs = web.get_view_breadcrumbs(instance.task)
        breadcrumbs.append(breadcrumb(self.get_edit_url(instance), "edit hardware todo"))
        return breadcrumbs

    def get_edit_finished_url(self, instance):
        self.assert_instance_type(instance)
        web = task_web()
        return web.get_view_url(instance.task)

    #################
    # DELETE ACTION #
    #################

    def get_delete_breadcrumbs(self, instance):
        self.assert_instance_type(instance)
        self.assert_instance_type(instance)
        web = task_web()
        breadcrumbs = web.get_view_breadcrumbs(instance.task)
        breadcrumbs.append(breadcrumb(self.get_delete_url(instance), "delete hardware todo"))
        return breadcrumbs

    def get_delete_finished_url(self, instance):
        self.assert_instance_type(instance)
        web = task_web()
        return web.get_view_url(instance.task)


########
# DATA #
########

class data_web(base_web):
    web_id = "data"
    model = models.data
    form = forms.data_form

    def get_instance(self):
        instance = models.data()
        instance.datetime = datetime.datetime.now()
        return instance

    ###############
    # LIST ACTION #
    ###############

    ###############
    # VIEW ACTION #
    ###############

    ##############
    # ADD ACTION #
    ##############

    ###############
    # EDIT ACTION #
    ###############

    #################
    # DELETE ACTION #
    #################

