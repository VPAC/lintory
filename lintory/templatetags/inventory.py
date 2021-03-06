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

from django import template
from django.utils.safestring import mark_safe
from django.utils.http import urlquote
from django.utils.html import conditional_escape
from django.contrib.contenttypes.models import ContentType

from lintory import models, tables, webs

from django.db.models import Q

register = template.Library()

@register.tag
def has_svg_file(parser, token):
    try:
        tag_name, result, location = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly two arguments" % token.contents.split()[0]
    return has_svg_file_node(location, result)

class has_svg_file_node(template.Node):
    def __init__(self, location, result):
        self.result = result
        self.location = template.Variable(location)
    def render(self, context):
        result = self.result
        location = self.location.resolve(context)

        web = webs.location_web()
        context[result] = web.has_svg_file(location)
        return ''

@register.simple_tag
def get_svg_url(instance):
    web = webs.get_web_from_object(instance)
    return mark_safe(web.get_svg_url(instance))

@register.filter
def bytes(value):
    units = "bytes"

    value=int(value)

    if value > 1000:
        value = value / 1000
        units = "KB"

    if value > 1000:
        value = value / 1000
        units = "MB"

    if value > 1000:
        value = value / 1000
        units = "GB"

    if value > 1000:
        value = value / 1000
        units = "TB"

    return mark_safe(u"%s %s"%(value, units))

def defaults(context):
    return {
        'user': context['user'],
        'perms': context['perms'],
        'request': context['request'],
        'MEDIA_URL': context['MEDIA_URL'],
    }

@register.inclusion_tag('django_webs/show_object_list.html', takes_context=True)
def show_hardware_list(context, object_list, sort="hardware_sort"):
    request = context['request']
    web = webs.hardware_web()
    dict = defaults(context)
    dict['table'] = tables.hardware(request, web, object_list,request.GET.get(sort))
    dict['rows'] = dict['table'].rows
    dict['web'] = web
    dict['sort'] = sort
    return dict

@register.inclusion_tag('django_webs/show_object_list.html', takes_context=True)
def show_location_list(context, object_list, sort="location_sort"):
    request = context['request']
    web = webs.location_web()
    dict = defaults(context)
    dict['table'] = tables.location(request, web, object_list,request.GET.get(sort))
    dict['rows'] = dict['table'].rows
    dict['web'] = web
    dict['sort'] = sort
    return dict

@register.inclusion_tag('django_webs/show_object_list.html', takes_context=True)
def show_license_list(context, object_list, sort="license_sort"):
    request = context['request']
    web = webs.license_web()
    dict = defaults(context)
    dict['table'] = tables.license(request, web, object_list,request.GET.get(sort))
    dict['rows'] = dict['table'].rows
    dict['web'] = web
    dict['sort'] = sort
    return dict

@register.inclusion_tag('django_webs/show_object_list.html', takes_context=True)
def show_license_key_list(context, object_list, sort="license_key_sort"):
    request = context['request']
    web = webs.license_key_web()
    dict = defaults(context)
    dict['table'] = tables.license_key(request, web, object_list,request.GET.get(sort))
    dict['rows'] = dict['table'].rows
    dict['web'] = web
    dict['sort'] = sort
    return dict

@register.inclusion_tag('django_webs/show_object_list.html', takes_context=True)
def show_software_list(context, object_list, sort="software_sort"):
    request = context['request']
    web = webs.software_web()
    dict = defaults(context)
    dict['table'] = tables.software(request, web, object_list,request.GET.get(sort))
    dict['rows'] = dict['table'].rows
    dict['web'] = web
    dict['sort'] = sort
    return dict

@register.inclusion_tag('django_webs/show_object_list.html', takes_context=True)
def show_software_installation_list(context, object_list, sort="software_installation_sort"):
    request = context['request']
    web = webs.software_installation_web()
    dict = defaults(context)
    dict['table'] = tables.software_installation(request, web, object_list,request.GET.get(sort))
    dict['rows'] = dict['table'].rows
    dict['web'] = web
    dict['sort'] = sort
    return dict

@register.inclusion_tag('django_webs/show_object_list.html', takes_context=True)
def show_task_list(context, object_list, sort="task_sort"):
    request = context['request']
    web = webs.task_web()
    dict = defaults(context)
    dict['table'] = tables.task(request, web, object_list,request.GET.get(sort))
    dict['rows'] = dict['table'].rows
    dict['web'] = web
    dict['sort'] = sort
    return dict

@register.inclusion_tag('django_webs/show_object_list.html', takes_context=True)
def show_hardware_task_list(context, object_list, sort="hardware_task_sort"):
    request = context['request']
    web = webs.hardware_task_web()
    dict = defaults(context)
    dict['table'] = tables.hardware_task(request, web, object_list,request.GET.get(sort))
    dict['rows'] = dict['table'].rows
    dict['web'] = web
    dict['sort'] = sort
    return dict

@register.inclusion_tag('lintory/show_history.html', takes_context=True)
def show_history(context, object):
    dict = defaults(context)
    dict['type_id'] = ContentType.objects.get_for_model(object)
    dict['object'] = object
    return dict

@register.inclusion_tag('django_webs/show_object_list.html', takes_context=True)
def show_os_list(context, object_list, sort="os_sort"):
    request = context['request']
    web = webs.os_web()
    dict = defaults(context)
    dict['table'] = tables.os(request, web, object_list,request.GET.get(sort))
    dict['rows'] = dict['table'].rows
    dict['web'] = web
    dict['sort'] = sort
    return dict

@register.inclusion_tag('django_webs/show_object_list.html', takes_context=True)
def show_data_list(context, object_list, sort="data_sort"):
    request = context['request']
    web = webs.data_web()
    dict = defaults(context)
    dict['table'] = tables.data(request, web, object_list,request.GET.get(sort))
    dict['rows'] = dict['table'].rows
    dict['web'] = web
    dict['sort'] = sort
    return dict

@register.tag
def get_licenses_by_software_owner(parser, token):
    try:
        tag_name, tag, software, owner = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly three arguments" % token.contents.split()[0]
    return get_licenses_by_software_owner_node(tag,software,owner)

class get_licenses_by_software_owner_node(template.Node):
    def __init__(self, tag, software, owner):
        self.tag = template.Variable(tag)
        self.software = template.Variable(software)
        self.owner = template.Variable(owner)
    def render(self, context):
        tag = self.tag.resolve(context)
        software = self.software.resolve(context)
        owner = self.owner.resolve(context)

        # get licenses for this software owned by specified owner
        if isinstance(owner,models.Nobody):
            licenses = models.license.objects.filter(
                license_key__isnull=False,
                license_key__software=software,owner__isnull=True).distinct()
        else:
            licenses = models.license.objects.filter(license_key__software=software,owner=owner).distinct()

        # are there are licenses for this software?
        licenses_count = models.license.objects.filter(license_key__software=software).distinct().count()
        if licenses_count == 0:
            # If no licenses, assume we have unlimited installs available
            max = None
            found = 0
            left = None
            # note if we got here then licenses.count() must also be 0
        else:
            # otherwise we default to 0 maximum installs and start counting
            max = 0
            found = 0
            left = 0
            for license in licenses:
                value = license.software_installations_found()
                if value is None:
                    found = None
                elif max is not None:
                    found = found + value

                value = license.installations_max
                if value is None:
                    max = None
                elif max is not None:
                    max = max + value

                value = license.software_installations_left()
                if value is None:
                    left = None
                elif max is not None:
                    left = left + value

        # add unlicenced installs, so they don't get forgotten
        unlicensed_installations = models.software_installation.objects.filter(
            Q(active=True,software=software,license_key__isnull=True)
        )

        found = found + unlicensed_installations.count()

        if left is not None:
            left = left - unlicensed_installations.count()

        # save results to context variables
        context[tag] = licenses
        context[tag+"_found"] = found
        context[tag+"_max"] = max
        context[tag+"_left"] = left
        return ''

@register.tag
def get_license_keys_by_software_owner(parser, token):
    try:
        tag_name, tag, software, owner = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly three arguments" % token.contents.split()[0]
    return get_license_keys_by_software_owner_node(tag,software,owner)

class get_license_keys_by_software_owner_node(template.Node):
    def __init__(self, tag, software, owner):
        self.tag = template.Variable(tag)
        self.software = template.Variable(software)
        self.owner = template.Variable(owner)
    def render(self, context):
        tag = self.tag.resolve(context)
        software = self.software.resolve(context)
        owner = self.owner.resolve(context)

        if isinstance(owner,models.Nobody):
            license_keys = models.license_key.objects.filter(software=software,license__owner__isnull=True)
        else:
            license_keys = models.license_key.objects.filter(software=software,license__owner=owner)

        context[tag] = license_keys
        return ''

@register.tag
def get_active_software_installations_by_software_owner(parser, token):
    try:
        tag_name, tag, software, owner = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly three arguments" % token.contents.split()[0]
    return get_active_software_installations_by_software_owner_node(tag,software,owner)

class get_active_software_installations_by_software_owner_node(template.Node):
    def __init__(self, tag, software, owner):
        self.tag = template.Variable(tag)
        self.software = template.Variable(software)
        self.owner = template.Variable(owner)
    def render(self, context):
        tag = self.tag.resolve(context)
        software = self.software.resolve(context)
        owner = self.owner.resolve(context)

        if isinstance(owner,models.Nobody):
            software_installations = models.software_installation.objects.filter(
                    Q(active=True,software=software,license_key__isnull=False,license_key__license__owner__isnull=True) |
                    Q(active=True,software=software,license_key__isnull=True))
        else:
            software_installations = models.software_installation.objects.filter(
                    Q(active=True,software=software,license_key__license__owner=owner) |
                    Q(active=True,software=software,license_key__isnull=True))

        context[tag] = software_installations
        return ''


