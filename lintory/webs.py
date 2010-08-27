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

from django.core.urlresolvers import reverse
from django.db import models
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404

# META INFORMATION FOR MODELS

class breadcrumb(object):
    def __init__(self, url, name):
        self.url = url
        self.name = name

#####################
# PERMISSION CHECKS #
#####################

def HttpErrorResponse(request, breadcrumbs, error_list):
    t = loader.get_template('lintory/error.html')
    c = RequestContext(request, {
            'title': 'Access denied',
            'error_list': error_list,
            'breadcrumbs': breadcrumbs
    })
    return HttpResponseForbidden(t.render(c))

def check_list_perms(request, breadcrumbs, web):
    error_list = []
    if not web.has_list_perms(request.user):
        error_list.append("You cannot list %s objects"%(webs.single_name()))

    if len(error_list) > 0:
        return HttpErrorResponse(request, breadcrumbs, error_list)
    else:
        return None

def check_view_perms(request, breadcrumbs, web):
    error_list = []
    if not web.has_view_perms(request.user):
        error_list.append("You cannot view a %s object"%(webs.single_name()))

    if len(error_list) > 0:
        return HttpErrorResponse(request, breadcrumbs, error_list)
    else:
        return None

def check_add_perms(request, breadcrumbs, web):
    error_list = []
    if not web.has_add_perms(request.user):
        error_list.append("You cannot add a %s object"%(webs.single_name()))

    if len(error_list) > 0:
        return HttpErrorResponse(request, breadcrumbs, error_list)
    else:
        return None

def check_edit_perms(request, breadcrumbs, web):
    error_list = []
    if not web.has_edit_perms(request.user):
        error_list.append("You cannot edit a %s object"%(webs.single_name()))

    if len(error_list) > 0:
        return HttpErrorResponse(request, breadcrumbs, error_list)
    else:
        return None

def check_delete_perms(request, breadcrumbs, web):
    error_list = []
    if not web.has_delete_perms(request.user):
        error_list.append("You cannot delete a %s object"%(webs.single_name()))

    if len(error_list) > 0:
        return HttpErrorResponse(request, breadcrumbs, error_list)
    else:
        return None

################
# BASE METHODS #
################
class base_web(object):
    verbose_name = None
    verbose_name_plural = None

    def assert_subject_type(self, subject):
        type_name = type(subject).__name__
        expected_type = self.web_id

        if type_name != expected_type:
            raise RuntimeError("Expected type %s but got '%s'"%(expected_type,type_name))

    def single_name(self):
        if self.verbose_name is not None:
            return self.verbose_name

        web_id = self.web_id
        return web_id.replace("_", " ")

    def plural_name(self):
        if self.verbose_name_plural is not None:
            return self.verbose_name_plural

        return self.single_name() + 's'

    def has_name_perms(self, user, name):
        if user.is_authenticated() and user.has_perm('inventory.%s_%s'%(name, self.web_id)):
            return True
        else:
            return False

    def get_breadcrumbs(self):
        breadcrumbs = []
        breadcrumbs.append(breadcrumb(reverse("lintory_root"), "home"))
        breadcrumbs.append(breadcrumb(reverse(self.web_id+"_list"), self.plural_name()))
        return breadcrumbs

    ###############
    # LIST ACTION #
    ###############

    def has_list_perms(self, user):
        return True

    def get_list_breadcrumbs(self):
        return self.get_breadcrumbs()

    def get_list_buttons(self, user):
        buttons = []

        if self.has_add_perms(user):
            buttons.append({
                'class': 'addlink',
                'text': 'Add %s'%(self.single_name()),
                'link': self.get_add_url(),
            })

        return buttons

    ###############
    # VIEW ACTION #
    ###############

    def has_view_perms(self, user):
        return True

    # get the URL to display this object
    # note this may not always make sense
    @models.permalink
    def get_view_url(self, subject):
        self.assert_subject_type(subject)
        return(self.web_id+'_detail', [ str(subject.pk) ])

    # get the breadcrumbs to show while displaying this object
    def get_view_breadcrumbs(self, subject):
        self.assert_subject_type(subject)
        breadcrumbs = self.get_breadcrumbs()
        breadcrumbs.append(breadcrumb(self.get_view_url(subject), subject))
        return breadcrumbs

    def get_view_buttons(self, user, subject):
        buttons = []

        if self.has_edit_perms(user):
            buttons.append({
                'class': 'changelink',
                'text': 'Edit',
                'link': self.get_edit_url(subject),
            })

        if self.has_delete_perms(user):
            buttons.append({
                'class': 'deletelink',
                'text': 'Delete',
                'link': self.get_delete_url(subject),
            })

        return buttons

    ##############
    # ADD ACTION #
    ##############

    def has_add_perms(self, user):
        return self.has_name_perms(user, "add")

    @models.permalink
    def get_add_url(self):
        return(self.web_id+"_add",)

    def get_add_breadcrumbs(self, **kwargs):
        breadcrumbs = self.get_breadcrumbs()
        breadcrumbs.append(breadcrumb(self.get_add_url(**kwargs), "add"))
        return breadcrumbs

    ###############
    # EDIT ACTION #
    ###############

    def has_edit_perms(self, user):
        return self.has_name_perms(user, "edit")

    # get the URL to edit this object
    @models.permalink
    def get_edit_url(self, subject):
        self.assert_subject_type(subject)
        return(self.web_id+'_edit', [ str(subject.pk) ])

    # find link we should go to after editing this object
    def get_edit_finished_url(self, subject):
        self.assert_subject_type(subject)
        return self.get_view_url(subject)

    # get breadcrumbs to show while editing this object
    def get_edit_breadcrumbs(self, subject):
        self.assert_subject_type(subject)
        breadcrumbs = self.get_view_breadcrumbs(subject)
        breadcrumbs.append(breadcrumb(self.get_edit_url(subject), "edit"))
        return breadcrumbs

    #################
    # DELETE ACTION #
    #################

    def has_delete_perms(self, user):
        return self.has_name_perms(user, "delete")

    # get the URL to delete this object
    @models.permalink
    def get_delete_url(self, subject):
        self.assert_subject_type(subject)
        return(self.web_id+'_delete', [ str(subject.pk) ])

    # find link we should go to after deleting object
    @models.permalink
    def get_deleted_url(self, subject):
        self.assert_subject_type(subject)
        return(self.web_id+"_list",)

    # get breadcrumbs to show while deleting this object
    def get_delete_breadcrumbs(self, subject):
        self.assert_subject_type(subject)
        breadcrumbs = self.get_view_breadcrumbs(subject)
        breadcrumbs.append(breadcrumb(self.get_delete_url(subject), "delete"))
        return breadcrumbs

    #####################
    # GENERIC FUNCTIONS #
    #####################

    def object_list(self, request, filter, table, template=None, kwargs={}, context={}):
        breadcrumbs = self.get_list_breadcrumbs(**kwargs)

        error = check_list_perms(request, breadcrumbs, self)
        if error is not None:
            return error

        if template is None:
            template='lintory/object_list.html'

        paginator = Paginator(table.rows, 50) # Show 50 objects per page

        # Make sure page request is an int. If not, deliver first page.
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        # If page request (9999) is out of range, deliver last page of results.
        try:
            page_obj = paginator.page(page)
        except (EmptyPage, InvalidPage):
            page_obj = paginator.page(paginator.num_pages)

        defaults = {
                'web': self,
                'filter': filter,
                'table': table,
                'page_obj': page_obj,
                'breadcrumbs': breadcrumbs,
        }
        defaults.update(context)
        return render_to_response(template, defaults,
                context_instance=RequestContext(request))

    def object_view(self, request, subject, template=None):
        self.assert_subject_type(subject)
        breadcrumbs = self.get_view_breadcrumbs(subject)

        error = check_view_perms(request, breadcrumbs, self)
        if error is not None:
            return error

        if template is None:
            template='lintory/'+self.web_id+'_detail.html'
        return render_to_response(template, {
                'object': subject,
                'web': self,
                'breadcrumbs': breadcrumbs,
                },context_instance=RequestContext(request))

    def object_add(self, request, modal_form, get_defaults=None, pre_save=None, template=None, kwargs={}):
        breadcrumbs = self.get_add_breadcrumbs(**kwargs)

        if template is None:
            template='lintory/object_edit.html'

        error = check_add_perms(request, breadcrumbs, self)
        if error is not None:
            return error

        if request.method == 'POST':
            form = modal_form(request.POST, request.FILES)

            if form.is_valid():
                valid = True
                instance = form.save(commit=False)

                if pre_save is not None:
                    valid = pre_save(instance=instance, form=form)

                if valid:
                    instance.save()
                    url=self.get_edited_url(instance)
                    return HttpResponseRedirect(url)
        else:
            if get_defaults is None:
                form = modal_form()
            else:
                instance = get_defaults()
                form = modal_form(instance=instance)

        return render_to_response(template, {
                'object': None, 'web': self,
                'breadcrumbs': breadcrumbs,
                'form' : form,
                'media' : form.media,
                },context_instance=RequestContext(request))

    def object_edit(self, request, subject, modal_form, pre_save=None, template=None):
        self.assert_subject_type(subject)
        breadcrumbs = self.get_edit_breadcrumbs(subject)

        if template is None:
            template='lintory/object_edit.html'

        error = check_edit_perms(request, breadcrumbs, self)
        if error is not None:
            return error

        if request.method == 'POST':
            form = modal_form(request.POST, request.FILES, instance=subject)
            if form.is_valid():
                valid = True
                instance = form.save(commit=False)

                if pre_save is not None:
                    valid = pre_save(instance=instance, form=form)

                if valid:
                    instance.save()
                    url = self.get_edited_url(subject)
                    return HttpResponseRedirect(url)
        else:
            form = modal_form(instance=subject)

        return render_to_response(template, {
                'object': subject,
                'web': self,
                'breadcrumbs': breadcrumbs,
                'form' : form,
                'media' : form.media,
                },context_instance=RequestContext(request))

    def object_delete(self, request, subject, template=None):
        self.assert_subject_type(subject)
        breadcrumbs = self.get_delete_breadcrumbs(subject)

        if template is None:
            template='lintory/object_confirm_delete.html'

        error = check_delete_perms(request, breadcrumbs, self)
        if error is not None:
            return error

        errorlist = []
        if request.method == 'POST':
            errorlist = subject.check_delete()
            if len(errorlist) == 0:
                url = self.get_deleted_url(subject)
                subject.delete()
                return HttpResponseRedirect(url)

        return render_to_response(template, {
                'object': subject,
                'breadcrumbs': breadcrumbs,
                'errorlist': errorlist,
                },context_instance=RequestContext(request))

#########
# PARTY #
#########

class party_web(base_web):
    web_id = "party"
    verbose_name_plural = "parties"

    def get_view_buttons(self, user, subject):
        buttons = super(party_web, self).get_view_buttons(user, subject)

        if self.has_view_perms(user):
            buttons.insert(0,{
                'class': 'viewlink',
                'text': 'Software',
                'link': self.get_software_list_url(subject),
            })

        return buttons

    @models.permalink
    def get_software_list_url(self, subject):
        self.assert_subject_type(subject)
        return('party_software_list', [ str(subject.pk) ])

    @models.permalink
    def get_software_view_url(self, subject, software):
        self.assert_subject_type(subject)
        return('party_software_detail', [ str(subject.pk), str(software.pk) ])

###########
# HISTORY #
###########

class history_item_web(base_web):
    web_id = "history_item"

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

    @models.permalink
    def get_add_url(self, object):
        # note: object is the object containing history item, not the history item
        o_web = get_web_from_object(object)
        return("history_item_add", [ o_web.web_id, object.pk ] )

    def get_add_breadcrumbs(self, object):
        # note: object is the object containing history item, not the history item
        o_web = get_web_from_object(object)
        breadcrumbs = o_web.get_view_breadcrumbs(object)
        breadcrumbs.append(breadcrumb(self.get_add_url(object), "add history"))
        return breadcrumbs

    ###############
    # EDIT ACTION #
    ###############

    @models.permalink
    def get_edit_url(self, subject):
        self.assert_subject_type(subject)
        return('history_item_edit', [ str(subject.pk) ])

    def get_edited_url(self, subject):
        self.assert_subject_type(subject)
        web = get_web_from_object(subject.content_object)
        return web.get_view_url(subject.content_object)

    # get breadcrumbs to show while editing this object
    def get_edit_breadcrumbs(self, subject):
        self.assert_subject_type(subject)
        breadcrumbs = self.get_view_breadcrumbs(subject)
        breadcrumbs.append(breadcrumb(self.get_edit_url(subject), "edit history"))
        return breadcrumbs

    #################
    # DELETE ACTION #
    #################

    @models.permalink
    def get_delete_url(self, subject):
        self.assert_subject_type(subject)
        return('history_item_delete', [ str(subject.pk) ])

    def get_deleted_url(self, subject):
        self.assert_subject_type(subject)
        web = get_web_from_object(subject.content_object)
        return web.get_view_url(subject.content_object)

    # get breadcrumbs to show while deleting this object
    def get_delete_breadcrumbs(self, subject):
        self.assert_subject_type(subject)
        breadcrumbs = self.get_view_breadcrumbs(subject)
        breadcrumbs.append(breadcrumb(self.get_delete_url(subject), "delete history"))
        return breadcrumbs



##########
# VENDOR #
##########

class vendor_web(base_web):
    web_id = "vendor"

############
# LOCATION #
############

class location_web(base_web):
    web_id = "location"

    ###############
    # LIST ACTION #
    ###############

    ###############
    # VIEW ACTION #
    ###############

    @models.permalink
    def get_svg_url(self, subject):
        self.assert_subject_type(subject)
        return('location_svg', [ str(subject.pk) ])

    def get_view_breadcrumbs(self, subject):
        self.assert_subject_type(subject)

        breadcrumbs = []
        breadcrumbs.append(breadcrumb(reverse("lintory_root"), "home"))

        object=subject
        seen = {}
        while object is not None and object.pk not in seen:
            breadcrumbs.insert(1,breadcrumb(self.get_view_url(object),object))
            seen[object.pk] = True
            object = object.parent

        if object is not None:
            breadcrumbs.insert(1,breadcrumb(self.get_view_url(object), "ERROR"))

        return breadcrumbs

    def get_view_buttons(self, user, subject):
        buttons = super(location_web, self).get_view_buttons(user, subject)

        if self.has_add_perms(user):
            buttons.insert(0,{
                'class': 'addlink',
                'text': 'Add location',
                'link': self.get_add_url(subject),
            })

        return buttons

    ##############
    # ADD ACTION #
    ##############

    @models.permalink
    def get_add_url(self, parent):
        return(self.web_id+"_add", [ parent.pk ] )

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

    def get_deleted_url(self, subject):
        self.assert_subject_type(subject)
        if subject.parent is not None:
                return subject.parent.get_view_url()
        else:
                return reverse("lintory_root")

############
# HARDWARE #
############

class hardware_web(base_web):
    web_id = "hardware"
    verbose_name_plural = "hardware"

    def assert_subject_type(self, subject):
        type_name = type(subject).__name__
        expected_type = self.hardware_type

        if type_name != expected_type:
            raise RuntimeError("Expected type %s but got '%s'"%(expected_type,type_name))

    def single_name(self):
        if self.verbose_name is not None:
            return self.verbose_name

        hardware_type = self.hardware_type
        return hardware_type.replace("_", " ")

    def get_breadcrumbs(self):
        breadcrumbs = []
        breadcrumbs.append(breadcrumb(reverse("lintory_root"), "home"))
        breadcrumbs.append(breadcrumb(reverse("hardware_list"), "hardware"))
        return breadcrumbs

    ###############
    # LIST ACTION #
    ###############

    ###############
    # VIEW ACTION #
    ###############

    def get_view_buttons(self, user, subject):
        buttons = super(hardware_web, self).get_view_buttons(user, subject)

        if self.has_add_perms(user):
            buttons.insert(0,{
                'class': 'addlink',
                'text': 'Add hardware',
                'link': self.get_add_to_subject_url(subject),
            })

        if self.has_edit_perms(user):
            buttons.insert(1,{
                'class': 'changelink',
                'text': 'Install hardware',
                'link': self.get_install_url(subject),
            })

        return buttons

    ##############
    # ADD ACTION #
    ##############

    @models.permalink
    def get_add_url(self, type_id=None):
        if type_id==None:
            return("hardware_add",)
        else:
            return("hardware_type_add",[ type_id ])

    @models.permalink
    def get_add_to_subject_url(self, subject, type_id=None):
        if type_id is None:
            return('hardware_add', [ str(subject.pk) ])
        else:
            return('hardware_add', [ str(subject.pk), str(type_id) ])

    ###############
    # EDIT ACTION #
    ###############

    @models.permalink
    def get_install_url(self, subject):
        self.assert_subject_type(subject)
        return('hardware_install', [ str(subject.pk) ])

    #################
    # DELETE ACTION #
    #################


class motherboard_web(hardware_web):
    hardware_type = "motherboard"

class processor_web(hardware_web):
    hardware_type = "processor"

class video_controller_web(hardware_web):
    hardware_type = "video_controller"

class network_adaptor_web(hardware_web):
    hardware_type = "network_adaptor"

class storage_web(hardware_web):
    hardware_type = "storage"
    verbose_name_plural = "storage"

class power_supply_web(hardware_web):
    hardware_type = "power_supply"
    verbose_name_plural = "power supplies"

class computer_web(hardware_web):
    hardware_type = "computer"

class monitor_web(hardware_web):
    hardware_type = "monitor"

class multifunction_web(hardware_web):
    hardware_type = "multifunction"

class printer_web(hardware_web):
    hardware_type = "printer"

class scanner_web(hardware_web):
    hardware_type = "scanner"

class docking_station_web(hardware_web):
    hardware_type = "docking_station"

class camera_web(hardware_web):
    hardware_type = "camera"

######
# OS #
######

class os_web(base_web):
    web_id = "os"
    verbose_name_plural = "os"

    ###############
    # LIST ACTION #
    ###############

    ###############
    # VIEW ACTION #
    ###############

    def get_view_breadcrumbs(self, subject):
        self.assert_subject_type(subject)
        web = storage_web()
        breadcrumbs = web.get_view_breadcrumbs(subject.storage)
        breadcrumbs.append(breadcrumb(self.get_view_url(subject), subject))
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

    def get_deleted_url(self, subject):
        return subject.storage.get_view_url()

############
# SOFTWARE #
############
class software_web(base_web):
    web_id = "software"
    verbose_name_plural = "software"

    ###############
    # LIST ACTION #
    ###############

    ###############
    # VIEW ACTION #
    ###############

    def get_view_buttons(self, user, subject):
        buttons = super(software_web, self).get_view_buttons(user, subject)

        if self.has_add_license_perms(user):
            buttons.append({
                'class': 'addlink',
                'text': 'Add license',
                'link': self.get_add_license_url(subject),
            })

        if self.has_add_software_installation_perms(user):
            buttons.append({
                'class': 'addlink',
                'text': 'Add installation',
                'link': self.get_add_software_installation_url(subject),
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

    @models.permalink
    def get_add_software_installation_url(self, subject):
        self.assert_subject_type(subject)
        return('software_add_software_installation', [ str(subject.pk) ])

    @models.permalink
    def get_add_license_url(self, subject):
        self.assert_subject_type(subject)
        return('software_add_license', [ str(subject.pk) ])

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

    ###############
    # LIST ACTION #
    ###############

    ###############
    # VIEW ACTION #
    ###############

    def get_view_buttons(self, user, subject):
        buttons = super(license_web, self).get_view_buttons(user, subject)

        if self.has_add_license_key_perms(user):
            buttons.append({
                'class': 'addlink',
                'text': 'Add key',
                'link': self.get_add_license_key_url(subject),
            })

        return buttons

    ##############
    # ADD ACTION #
    ##############

    def has_add_license_key_perms(self, user):
        web = license_web()
        return web.has_add_perms(user)

    @models.permalink
    def get_add_license_key_url(self, subject):
        self.assert_subject_type(subject)
        return('license_add_license_key', [ str(subject.pk) ])

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

    ###############
    # LIST ACTION #
    ###############

    ###############
    # VIEW ACTION #
    ###############

    def get_view_breadcrumbs(self, subject):
        self.assert_subject_type(subject)
        web = license_web()
        breadcrumbs = web.get_view_breadcrumbs(subject.license)
        breadcrumbs.append(breadcrumb(web.get_view_url(subject.license), subject))
        return breadcrumbs

    ##############
    # ADD ACTION #
    ##############

    @models.permalink
    def get_add_url(self, license):
        return("license_add_"+self.web_id, [ license.pk ] )

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

    def get_deleted_url(self, subject):
        return subject.software.get_view_url()

#########################
# SOFTWARE_INSTALLATION #
#########################

class software_installation_web(base_web):
    web_id = "software_installation"

    ###############
    # LIST ACTION #
    ###############

    ###############
    # VIEW ACTION #
    ###############

    def get_view_breadcrumbs(self, subject):
        self.assert_subject_type(subject)
        web = get_web_for_object(subject.software)
        breadcrumbs = web.get_breadcrumbs(subject.software)
        breadcrumbs.append(breadcrumb(web.get_view_url(subject.software), subject))
        return breadcrumbs

    ##############
    # ADD ACTION #
    ##############

    @models.permalink
    def get_add_url(self, software):
        return("software_add_"+self.web_id, [ software.pk ] )

    def get_add_breadcrumbs(self, **kwargs):
        breadcrumbs = self.get_breadcrumbs(**kwargs)
        breadcrumbs.append(breadcrumb(self.get_add_url(**kwargs), "add installation"))
        return breadcrumbs

    ###############
    # EDIT ACTION #
    ###############

    @models.permalink
    def get_edit_license_key_url(self, subject):
        self.assert_subject_type(subject)
        return('software_installation_edit_license_key', [ str(subject.pk) ])

    def get_edited_url(self, subject):
        self.assert_subject_type(subject)
        return subject.software.get_view_url()

    def get_edit_breadcrumbs(self, subject):
        self.assert_subject_type(subject)
        breadcrumbs = subject.get_breadcrumbs()
        breadcrumbs.append(breadcrumb(subject.get_edit_url(), "edit installation"))
        return breadcrumbs


    #################
    # DELETE ACTION #
    #################

    def get_deleted_url(self, subject):
        self.assert_subject_type(subject)
        return subject.software.get_view_url()

    def get_delete_breadcrumbs(self, subject):
        self.assert_subject_type(subject)
        breadcrumbs = subject.get_breadcrumbs()
        breadcrumbs.append(breadcrumb(subject.get_delete_url(), "delete installation"))
        return breadcrumbs


########
# TASK #
########

class task_web(base_web):
    web_id = "task"

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

    @models.permalink
    def get_add_hardware_url(self, subject):
        return('task_add_hardware', [ str(subject.pk) ])

    #################
    # DELETE ACTION #
    #################


#################
# HARDWARE_TASK #
#################

class hardware_task_web(base_web):
    web_id = "hardware_task"

    ###############
    # LIST ACTION #
    ###############

    ###############
    # VIEW ACTION #
    ###############

    def get_view_breadcrumbs(self, subject):
        self.assert_subject_type(subject)
        web = get_web_for_object(subject.task)
        breadcrumbs = web.get_breadcrumbs(subject.task)
        breadcrumbs.append(breadcrumb(web.get_view_url(subject.task), subject))
        return breadcrumbs

    ##############
    # ADD ACTION #
    ##############

    @models.permalink
    def get_add_url(self, task):
        return("task_add_hardware", [ task.pk ] )

    def get_add_breadcrumbs(self, **kwargs):
        breadcrumbs = self.get_breadcrumbs(**kwargs)
        breadcrumbs.append(breadcrumb(self.get_add_url(**kwargs), "add hardware"))
        return breadcrumbs

    ###############
    # EDIT ACTION #
    ###############

    def get_edit_breadcrumbs(self, subject):
        self.assert_subject_type(subject)
        breadcrumbs = subject.get_breadcrumbs()
        breadcrumbs.append(breadcrumb(subject.get_edit_url(), "edit hardware todo"))
        return breadcrumbs

    def get_edited_url(self, subject):
        self.assert_subject_type(subject)
        web = task_web()
        return web.get_view_url(subject.task)

    #################
    # DELETE ACTION #
    #################

    def get_delete_breadcrumbs(self, subject):
        self.assert_subject_type(subject)
        breadcrumbs = subject.get_breadcrumbs()
        breadcrumbs.append(breadcrumb(subject.get_delete_url(), "delete hardware todo"))
        return breadcrumbs

    def get_deleted_url(self, subject):
        self.assert_subject_type(subject)
        web = task_web()
        return web.get_view_url(subject.task)


########
# DATA #
########

class data_web(base_web):
    web_id = "data"

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

###############
# OTHER STUFF #
###############
types = {
    'history': history_item_web,
    'party': party_web,
    'history_item': history_item_web,
    'vendor': vendor_web,
    'location': location_web,
    'hardware': hardware_web,
    'motherboard': motherboard_web,
    'processor': processor_web,
    'video_controller': video_controller_web,
    'network_adaptor': network_adaptor_web,
    'storage': storage_web,
    'power_supply': power_supply_web,
    'computer': computer_web,
    'monitor': monitor_web,
    'multifunction': multifunction_web,
    'printer': printer_web,
    'scanner': scanner_web,
    'docking_station': docking_station_web,
    'camera': camera_web,
    'os': os_web,
    'software': software_web,
    'license': license_web,
    'license_key': license_key_web,
    'software_installation': software_installation_web,
    'task': task_web,
    'hardware_task': hardware_task_web,
    'data': data_web,
}

def get_web_from_object(self):
    type_name = type(self).__name__
    return types[type_name]()


