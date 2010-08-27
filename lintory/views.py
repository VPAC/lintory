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

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.encoding import smart_unicode
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect
from django.http import Http404, HttpResponseForbidden
from django.utils.html import escape
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import get_model
import django.views.generic.list_detail
import django.forms.util as util

from lintory import models, helpers, forms, eparty, tables, filters, webs

import datetime

def lintory_root(request):
    breadcrumbs = [ ]
    breadcrumbs.append(webs.breadcrumb(reverse("lintory_root"),"home"))

    return render_to_response('lintory/index.html', {
                                'breadcrumbs': breadcrumbs,
                                },
                        context_instance=RequestContext(request))

def get_object_by_string(type_id,object_id):
    model = get_model("lintory",type_id)
    if model is None:
        raise Http404("Bad model type '%s'"%(type_id))

    return get_object_or_404(model, pk=object_id)

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

#####################
# GENERIC FUNCTIONS #
#####################

def object_list(request, filter, table, web, template=None, kwargs={}, context={}):
    breadcrumbs = web.get_list_breadcrumbs(**kwargs)

    error = check_list_perms(request, breadcrumbs, web)
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
            'web': web,
            'filter': filter,
            'table': table,
            'page_obj': page_obj,
            'breadcrumbs': breadcrumbs,
    }
    defaults.update(context)
    return render_to_response(template, defaults,
            context_instance=RequestContext(request))

def object_detail(request, object, template=None):
    web=webs.get_web_from_object(object)
    breadcrumbs = web.get_view_breadcrumbs(object)

    error = check_view_perms(request, breadcrumbs, web)
    if error is not None:
        return error

    if template is None:
        template='lintory/'+web.web_id+'_detail.html'
    return render_to_response(template, {
            'object': object,
            'web': web,
            'breadcrumbs': breadcrumbs,
            },context_instance=RequestContext(request))

def object_add(request, web, modal_form, get_defaults=None, pre_save=None, template=None, kwargs={}):
    breadcrumbs = web.get_add_breadcrumbs(**kwargs)

    if template is None:
        template='lintory/object_edit.html'

    error = check_add_perms(request, breadcrumbs, web)
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
                url=web.get_edited_url(instance)
                return HttpResponseRedirect(url)
    else:
        if get_defaults is None:
            form = modal_form()
        else:
            instance = get_defaults()
            form = modal_form(instance=instance)

    return render_to_response(template, {
            'object': None, 'web': web,
            'breadcrumbs': breadcrumbs,
            'form' : form,
            'media' : form.media,
            },context_instance=RequestContext(request))

def object_edit(request, object, modal_form, pre_save=None, template=None):
    web=webs.get_web_from_object(object)
    breadcrumbs = web.get_edit_breadcrumbs(object)

    if template is None:
        template='lintory/object_edit.html'

    error = check_edit_perms(request, breadcrumbs, web)
    if error is not None:
        return error

    if request.method == 'POST':
        form = modal_form(request.POST, request.FILES, instance=object)
        if form.is_valid():
            valid = True
            instance = form.save(commit=False)

            if pre_save is not None:
                valid = pre_save(instance=instance, form=form)

            if valid:
                instance.save()
                url = web.get_edited_url(object)
                return HttpResponseRedirect(url)
    else:
        form = modal_form(instance=object)

    return render_to_response(template, {
            'object': object,
            'web': web,
            'breadcrumbs': breadcrumbs,
            'form' : form,
            'media' : form.media,
            },context_instance=RequestContext(request))

def object_delete(request, object, template=None):
    web=webs.get_web_from_object(object)
    breadcrumbs = web.get_delete_breadcrumbs(object)

    if template is None:
        template='lintory/object_confirm_delete.html'

    error = check_delete_perms(request, breadcrumbs, web)
    if error is not None:
        return error

    errorlist = []
    if request.method == 'POST':
        errorlist = object.check_delete()
        if len(errorlist) == 0:
            url = web.get_deleted_url(object)
            object.delete()
            return HttpResponseRedirect(url)

    return render_to_response(template, {
            'object': object,
            'breadcrumbs': breadcrumbs,
            'errorlist': errorlist,
            },context_instance=RequestContext(request))

###########
# HISTORY #
###########

def history_item_add(request, type_id, object_id):
    object = get_object_by_string(type_id,object_id)
    modal_form = forms.history_item_form

    def pre_save(instance, form):
        instance.content_type = ContentType.objects.get_for_model(object)
        instance.object_pk = object.pk
        instance.date = datetime.datetime.now()
        return True

    web = webs.history_item_web()
    return object_add(request, web, modal_form, pre_save=pre_save, kwargs={ 'object': object })

def history_item_edit(request, history_item_id):
    history_item = get_object_or_404(models.history_item, pk=history_item_id)
    return object_edit(request, history_item, forms.history_item_form_with_date)

def history_item_delete(request, history_item_id):
    history_item = get_object_or_404(models.history_item, pk=history_item_id)
    return object_delete(request, history_item)

#########
# PARTY #
#########

def party_list(request):
    web = webs.party_web()
    filter = filters.party(request.GET or None)
    table = tables.party(request.user, web, filter.qs, order_by=request.GET.get('sort'))
    return object_list(request, filter, table, web)

def party_detail(request, object_id):
    if object_id != "none":
        object = get_object_or_404(models.party, pk=object_id)
    else:
        object = models.Nobody()

    return object_detail(request, object)

def party_add(request):
    modal_form = forms.party_form
    return object_add(request, webs.party_web(), modal_form)

def party_edit(request,object_id):
    object = get_object_or_404(models.party, pk=object_id)
    return object_edit(request, object, forms.party_form)

def party_delete(request,object_id):
    object = get_object_or_404(models.party, pk=object_id)
    return object_delete(request, object)

def party_software_list(request, object_id):
    if object_id != "none":
        object = get_object_or_404(models.party, pk=object_id)
    else:
        object = models.Nobody()

    template='lintory/party_software_list.html'

    web = webs.party_web()
    breadcrumbs = web.get_view_breadcrumbs(object)
    breadcrumbs.append(webs.breadcrumb(web.get_software_list_url(object),"software list"))

    return render_to_response(template, {
            'object': object,
            'breadcrumbs': breadcrumbs,
            },context_instance=RequestContext(request))

def party_software_detail(request, object_id, software_id):
    if object_id != "none":
        object = get_object_or_404(models.party, pk=object_id)
    else:
        object = models.Nobody()

    template='lintory/party_software_detail.html'

    software = get_object_or_404(models.software, pk=software_id)

    web = webs.party_web()
    breadcrumbs = web.get_view_breadcrumbs(object)
    breadcrumbs.append(webs.breadcrumb(web.get_software_list_url(object),"software list"))
    breadcrumbs.append(webs.breadcrumb(web.get_software_view_url(object, software),software))

    return render_to_response(template, {
            'party': object,
            'software': software,
            'software_web': webs.software_web(),
            'breadcrumbs': breadcrumbs,
            },context_instance=RequestContext(request))


##########
# VENDOR #
##########

def vendor_list(request):
    web = webs.vendor_web()
    filter = filters.vendor(request.GET or None)
    table = tables.vendor(request.user, web, filter.qs, order_by=request.GET.get('sort'))
    return object_list(request, filter, table, web)

def vendor_detail(request, object_id):
    object = get_object_or_404(models.vendor, pk=object_id)
    return object_detail(request, object)

def vendor_add(request):
    modal_form = forms.vendor_form
    return object_add(request, webs.vendor_web(), modal_form)

def vendor_edit(request,object_id):
    object = get_object_or_404(models.vendor, pk=object_id)
    return object_edit(request, object, forms.vendor_form)

def vendor_delete(request,object_id):
    object = get_object_or_404(models.vendor, pk=object_id)
    return object_delete(request, object)

########
# TASK #
########

def task_list(request):
    web = webs.task_web()
    filter = filters.task(request.GET or None)
    table = tables.task(request.user, web, filter.qs, order_by=request.GET.get('sort'))
    return object_list(request, filter, table, web)

def task_detail(request, object_id):
    object = get_object_or_404(models.task, pk=object_id)
    return object_detail(request, object)

def task_add(request):
    modal_form = forms.task_form
    return object_add(request, webs.task_web(), modal_form)

def task_edit(request,object_id):
    object = get_object_or_404(models.task, pk=object_id)
    return object_edit(request, object, forms.task_form)

def task_delete(request,object_id):
    object = get_object_or_404(models.task, pk=object_id)
    return object_delete(request, object)

#################
# HARDWARE_TASK #
#################

def task_add_hardware(request, object_id):
    task = get_object_or_404(models.task, pk=object_id)
    modal_form = forms.hardware_task_form

    def get_defaults():
        instance = models.hardware_task()
        instance.task = task
        return instance

    return object_add(request, webs.hardware_task_web(), modal_form, get_defaults, kwargs={ 'task': task })

def hardware_task_edit(request,object_id):
    object = get_object_or_404(models.hardware_task, pk=object_id)
    return object_edit(request, object, forms.hardware_task_form)

def hardware_task_delete(request,object_id):
    object = get_object_or_404(models.hardware_task, pk=object_id)
    return object_delete(request, object)

############
# LOCATION #
############

def location_detail(request, object_id):
    object = get_object_or_404(models.location, pk=object_id)
    return object_detail(request, object)

def location_task_list(request, object_id):
    object = get_object_or_404(models.location, pk=object_id)

    breadcrumbs = object.get_breadcrumbs()
    breadcrumbs.append(models.breadcrumb(reverse('location_task_list',kwargs={'object_id':object_id}),"tasks"))

    return render_to_response('lintory/location_tasks.html', {
            'object': object,
            'breadcrumbs': breadcrumbs,
            'todo_hardware_tasks': 
                models.hardware_task.objects.filter(hardware__in=object.get_self_or_children_hardware(),date_complete__isnull=True),
            },context_instance=RequestContext(request))

def location_task(request, object_id, task_id):
    object = get_object_or_404(models.location, pk=object_id)
    task = get_object_or_404(models.task, pk=task_id)

    breadcrumbs = object.get_breadcrumbs()
    breadcrumbs.append(models.breadcrumb(reverse('location_task_list',kwargs={'object_id':object_id}),"tasks"))
    breadcrumbs.append(models.breadcrumb(reverse('location_task',kwargs={'object_id':object_id,'task_id':task_id}),task))

    return render_to_response('lintory/location_tasks.html', {
            'object': object,
            'task': task,
            'breadcrumbs': breadcrumbs,
            'todo_hardware_tasks': 
                models.hardware_task.objects.filter(hardware__in=object.get_self_or_children_hardware(),date_complete__isnull=True,task=task),
            },context_instance=RequestContext(request))

def location_redirect(request,object_id):
    object = get_object_or_404(models.location, pk=object_id)
    return HttpResponseRedirect(object.get_view_url())

def location_add(request, object_id):
    parent = get_object_or_404(models.location, pk=object_id)
    modal_form = forms.location_form

    def get_defaults():
        instance = models.location()
        instance.parent = parent
        return instance

    return object_add(request, webs.location_web(), modal_form, get_defaults=get_defaults, kwargs={ 'parent': parent })

def location_edit(request,object_id):
    object = get_object_or_404(models.location, pk=object_id)
    return object_edit(request, object, forms.location_form)

def location_delete(request,object_id):
    object = get_object_or_404(models.location, pk=object_id)
    return object_delete(request, object)

class location_hardware_lookup:
    def __init__(self, location):
        self.location = location

    def computers(self):
        list = models.computer.objects.filter(
                location=self.location,
                date_of_disposal__isnull=True)
        list = [ smart_unicode(i) for i in list ]
        return ",".join(list)

    def self_or_children_computers(self):
        location_list = self.location.get_self_or_children()
        list = models.computer.objects.filter(
                location__in=location_list,
                date_of_disposal__isnull=True)
        list = [ smart_unicode(i) for i in list ]
        return ",".join(list)

    # Short cut
    def url(self):
        return self.location.get_view_url()

    def __getitem__(self, key):
        value = getattr(self.location, key)
        if callable(value):
            if getattr(value, 'alters_data', False):
                raise IndexError("Method '%s' alters data"%(key))
            else:
                try: # method call (assuming no args required)
                    value = value()
                except TypeError: # arguments *were* required
                    # GOTCHA: This will also catch any TypeError
                    # raised in the function itself.
                    raise IndexError("Method '%s' raised TypeError"%(key))

        return value

class location_lookup:
    def __getitem__(self, key):
        try:
            location = models.location.objects.get(pk=key)
        except models.location.DoesNotExist, e:
            raise IndexError("Location %d not found"%(key))

        return location_hardware_lookup(location)

def location_svg(request, object_id):
    object = get_object_or_404(models.location, pk=object_id)

    # FIXME!
    if False:
        raise Http404

    return render_to_response('lintory/locations/%i.svg'%object.pk,
        mimetype= "image/svg+xml",
        context_instance=RequestContext(request,{
                    'location': location_lookup()
                }))

############
# HARDWARE #
############

# HARDWARE TYPE DATA

class type_data:
    def __init__(self, modal_form, type_class):
        self.modal_form = modal_form
        self.type_class = type_class

type_dict = {
    'motherboard': type_data(
        modal_form = forms.motherboard_form,
        type_class = models.motherboard,
    ),
    'processor': type_data(
        modal_form = forms.processor_form,
        type_class = models.processor,
    ),
    'video_controller': type_data(
        modal_form = forms.video_controller_form,
        type_class = models.video_controller,
    ),
    'network_adaptor': type_data(
        modal_form = forms.network_adaptor_form,
        type_class = models.network_adaptor,
    ),
    'storage': type_data(
        modal_form = forms.storage_form,
        type_class = models.storage,
    ),
    'computer': type_data(
        modal_form = forms.computer_form,
        type_class = models.computer,
    ),
    'power_supply': type_data(
        modal_form = forms.power_supply_form,
        type_class = models.power_supply,
    ),
    'monitor': type_data(
        modal_form = forms.monitor_form,
        type_class = models.monitor,
    ),
    'multifunction': type_data(
        modal_form = forms.multifunction_form,
        type_class = models.multifunction,
    ),
    'printer': type_data(
        modal_form = forms.printer_form,
        type_class = models.printer,
    ),
    'scanner': type_data(
        modal_form = forms.scanner_form,
        type_class = models.scanner,
    ),
    'docking_station': type_data(
        modal_form = forms.docking_station_form,
        type_class = models.docking_station,
    ),
    'camera': type_data(
        modal_form = forms.camera_form,
        type_class = models.camera,
    ),
}

# HARDWARE OBJECTS

def hardware_list(request):
    web = webs.hardware_web()
    filter = filters.hardware(request.GET or None)
    table = tables.hardware(request.user, web, filter.qs, order_by=request.GET.get('sort'))
    return object_list(request, filter, table, web)

def hardware_detail(request, object_id):
    object = get_object_or_404(models.hardware, pk=object_id)
    object = object.get_object()
    return object_detail(request, object)

def hardware_add(request, type_id=None, object_id=None):
    web = webs.hardware_web()
    if object_id is None:
        breadcrumbs = web.get_add_breadcrumbs()
    else:
        object = get_object_or_404(models.hardware, pk=object_id)
        breadcrumbs = web.get_view_breadcrumbs(object)
        breadcrumbs.append(webs.breadcrumb(web.get_add_to_subject_url(object,type_id),"add hardware"))

    if request.method == 'POST':
        form = forms.hardware_type_form(request.POST, request.FILES)

        if form.is_valid():
            new_type = form.cleaned_data['type']

            if object_id is None:
                url = type.get_add_url(new_type)
            else:
                url = object.get_add_url(new_type)
            return HttpResponseRedirect(url)
    else:
        form = forms.hardware_type_form()

    return render_to_response("lintory/hardware_type.html", {
            'breadcrumbs': breadcrumbs,
            'form' : form,
            'media' : form.media,
            },context_instance=RequestContext(request))

def hardware_edit(request, object_id):
    object = get_object_or_404(models.hardware, pk=object_id)
    type_id = object.type_id

    if type_id not in type_dict:
        raise Http404(u"Hardware type '%s' not found"%(type_id))

    object = object.get_object()
    modal_form = type_dict[type_id].modal_form
    return object_edit(request, object, modal_form)

def hardware_install(request, object_id):
    object = get_object_or_404(models.hardware, pk=object_id)
    error_list = [ ]
    pks = []

    if request.method == 'POST':
        pks = request.POST.getlist('pk')
        for pk in pks:
            requested_object = get_object_or_404(models.hardware, pk=pk)
            if requested_object.installed_on is not None:
                if requested_object.installed_on.pk != object.pk:
                    error_list.append(u"Cannot install '%s' as it is already installed on another computer"%(requested_object))
            else:
                requested_object.installed_on = object
                requested_object.save()

    web = webs.hardware_web()
    filter = filters.hardware(request.GET or {'is_installed': '3'})
    table = tables.hardware_list_form(pks, request.user, web, filter.qs, order_by=request.GET.get('sort'))
    return object_list(request, filter, table, web, template="lintory/hardware_list_form.html",
            context={ 'object': object, 'error_list': error_list })

def hardware_delete(request, object_id):
    object = get_object_or_404(models.hardware, pk=object_id)
    object = object.get_object()
    return object_delete(request, object)

def hardware_type_add(request, type_id, object_id=None):
    if type_id not in type_dict:
        raise Http404(u"Hardware type '%s' not found"%(type_id))

    if object_id is not None:
        object = get_object_or_404(models.hardware, pk=object_id)

    type_class = type_dict[type_id].type_class
    type = type_class.type
    modal_form = type_dict[type_id].modal_form

    def get_defaults():
        instance = type_class()
        if object_id is not None:
            instance.installed_on = object
        instance.seen_first = datetime.datetime.now()
        instance.seen_last = datetime.datetime.now()
        return instance

    return object_add(request, type, modal_form, get_defaults)

############
# SOFTWARE #
############

def software_list(request):
    web = webs.software_web()
    filter = filters.software(request.GET or None)
    table = tables.software(request.user, web, filter.qs, order_by=request.GET.get('sort'))
    return object_list(request, filter, table, web)

def software_detail(request, object_id):
    object = get_object_or_404(models.software, pk=object_id)
    return object_detail(request, object)

def software_add(request):
    modal_form = forms.software_form
    return object_add(request, webs.software_web(), modal_form)

def software_edit(request,object_id):
    object = get_object_or_404(models.software, pk=object_id)
    return object_edit(request, object, forms.software_form)

def software_delete(request,object_id):
    object = get_object_or_404(models.software, pk=object_id)
    return object_delete(request, object)

###########
# LICENSE #
###########

def license_list(request):
    web = webs.license_web()
    filter = filters.license(request.GET or None)
    table = tables.license(request.user, web, filter.qs, order_by=request.GET.get('sort'))
    return object_list(request, filter, table, web)

def license_detail(request, object_id):
    object = get_object_or_404(models.license, pk=object_id)
    return object_detail(request, object)

def license_add(request):
    modal_form = forms.license_form
    return object_add(request, webs.license_web(), modal_form)

def license_edit(request,object_id):
    object = get_object_or_404(models.license, pk=object_id)
    return object_edit(request, object, forms.license_form)

def software_add_license(request,object_id):
    object = get_object_or_404(models.software, pk=object_id)
    web = webs.software_web()
    breadcrumbs = web.get_view_breadcrumbs(object)
    breadcrumbs.append(webs.breadcrumb(web.get_add_license_url(object),"add software license"))

    error = check_add_perms(request, breadcrumbs, webs.license_web())
    if error is not None:
        return error

    if request.method == 'POST':
        form = forms.license_add_form(request.POST, request.FILES)

        if form.is_valid():
            valid = True
            # we try to get license_key first, in case something goes wrong.
            # if something goes wrong, no license will be created.
            key = form.cleaned_data['key'].strip()
            try:
                # try to find existing license for key
                if request.user.has_perm('lintory.edit_license_key'):
                    license_key = models.license_key.objects.get(key=key,software=object)
                else:
                    msg = u"License key exists and no permission to modify"
                    form._errors["key"] = util.ErrorList([msg])
                    valid = False
            except models.license_key.DoesNotExist, e:
                # no license found, we have to create one
                if request.user.has_perm('lintory.add_license_key'):
                    license_key = models.license_key()
                    license_key.software = object
                    license_key.key = key
                else:
                    msg = u"License key doesn't exist and no permission to add one"
                    form._errors["key"] = util.ErrorList([msg])
                    valid = False

            # Can we continue?
            if valid:
                # we need to create the license license
                license = models.license()
                license.vendor_tag = form.cleaned_data['vendor_tag']
                license.installations_max = form.cleaned_data['installations_max']
                license.version = form.cleaned_data['version']
                license.expires = form.cleaned_data['expires']
                license.owner = form.cleaned_data['owner']
                license.save()

                # Update license_key with license we just got
                license_key.license = license
                license_key.save()

                # we finished
                license_web = webs.license_web()
                url=license_web.get_view_url(license)
                return HttpResponseRedirect(url)
    else:
        form = forms.license_add_form()

    return render_to_response('lintory/object_edit.html', {
            'object': None, 'type': 'software license',
            'breadcrumbs': breadcrumbs,
            'form' : form,
            'media' : form.media,
            },context_instance=RequestContext(request))

def license_delete(request,object_id):
    object = get_object_or_404(models.license, pk=object_id)
    return object_delete(request, object)

###############
# LICENSE KEY #
###############

def license_key_detail(request, object_id):
    object = get_object_or_404(models.license_key, pk=object_id)
    return object_detail(request, object)

def license_add_license_key(request, object_id):
    license = get_object_or_404(models.license, pk=object_id)
    modal_form = forms.license_key_form

    def get_defaults():
        instance = models.license_key()
        instance.license = license
        return instance

    return object_add(request, webs.license_key_web(), modal_form, get_defaults, kwargs={ 'license': license })

def license_key_edit(request, object_id):
    object = get_object_or_404(models.license_key, pk=object_id)
    return object_edit(request, object, forms.license_key_form)

def license_key_delete(request,object_id):
    object = get_object_or_404(models.license_key, pk=object_id)
    return object_delete(request, object)

#########################
# SOFTWARE INSTALLATION #
#########################

def software_add_software_installation(request, object_id):
    software = get_object_or_404(models.software, pk=object_id)
    modal_form = forms.software_installation_form

    def get_defaults():
        instance = models.software_installation()
        instance.active = True
        instance.seen_first = datetime.datetime.now()
        instance.seen_last = datetime.datetime.now()
        return instance

    return object_add(request, webs.software_installation_web(), modal_form, get_defaults, kwargs={ 'software': software })

def software_installation_edit_license_key(request,object_id):
    object = get_object_or_404(models.software_installation, pk=object_id)
    breadcrumbs = object.software.get_breadcrumbs()
    breadcrumbs.append(models.breadcrumb(object.get_edit_license_key_url(),"edit license key"))

    web = webs.software_installation_web()
    error = check_edit_perms(request, breadcrumbs, web)
    if error is not None:
        return error

    if request.method == 'POST':
        form = forms.license_key_select_form(object.software,request.POST,request.FILES)
        if form.is_valid():
            if form.cleaned_data['key'] == "":
                license_key = None
            else:
                license_key = get_object_or_404(models.license_key, pk=form.cleaned_data['key'])

            object.license_key = license_key
            object.save()

            url = web.get_view_url(software)
            return HttpResponseRedirect(url)
    else:
        if object.license_key is None:
            key = ""
        else:
            key = object.license_key.pk

        form = forms.license_key_select_form(object.software,{'key': key})
        # fix me, choice may be null

    return render_to_response('lintory/object_edit.html', {
            'object': object,
            'breadcrumbs': breadcrumbs,
            'form' : form,
            'media' : form.media,
            },context_instance=RequestContext(request))

def software_installation_edit(request, object_id):
    object = get_object_or_404(models.software_installation, pk=object_id)

    def pre_save(instance, form):
        valid = True
        if instance.license_key is not None:
            if instance.license_key.software != instance.software:
                msg = u"Software must match license key %s"%(instance.license_key.software)
                form._errors["software"] = util.ErrorList([msg])
                valid = False
        return valid

    return object_edit(request, object, forms.software_installation_form, pre_save=pre_save)

def software_installation_delete(request,object_id):
    object = get_object_or_404(models.software_installation, pk=object_id)
    return object_delete(request, object)

######
# OS #
######

def os_detail(request, object_id):
    object = get_object_or_404(models.os, pk=object_id)
    return object_detail(request, object)

def os_add(request, object_id):
    storage = get_object_or_404(models.storage, pk=object_id)
    modal_form = forms.os_form

    def get_defaults():
        instance = models.os()
        instance.storage = storage
        instance.seen_first = datetime.datetime.now()
        instance.seen_last = datetime.datetime.now()
        return instance

    return object_add(request, webs.os_web(), modal_form, get_defaults, kwargs={ 'storage': storage })

def os_edit(request, object_id):
    object = get_object_or_404(models.os, pk=object_id)
    return object_edit(request, object, forms.os_form)

def os_delete(request,object_id):
    object = get_object_or_404(models.os, pk=object_id)
    return object_delete(request, object)


########
# DATA #
########

def data_list(request):
    web = webs.data_web()
    filter = filters.data(request.GET or None)
    table = tables.data(request.user, web, filter.qs, order_by=request.GET.get('sort'))
    return object_list(request, filter, table, web)

def data_detail(request, object_id):
    object = get_object_or_404(models.data, pk=object_id)
    return object_detail(request, object)

def data_add(request):
    modal_form = forms.data_form
    template = 'lintory/object_file_edit.html'

    def get_defaults():
        instance = models.data()
        instance.datetime = datetime.datetime.now()
        return instance

    return object_add(request, webs.data_web, modal_form, template=template, get_defaults=get_defaults)

def data_edit(request, object_id):
    template = 'lintory/object_file_edit.html'
    object = get_object_or_404(models.data, pk=object_id)
    return object_edit(request, object, forms.data_form, template=template)

def data_delete(request,object_id):
    object = get_object_or_404(models.data, pk=object_id)
    return object_delete(request, object)

