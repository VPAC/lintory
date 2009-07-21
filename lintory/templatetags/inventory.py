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

from lintory import models

from django.db.models import Q

register = template.Library()

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
    }

@register.inclusion_tag('lintory/show_error_list.html')
def show_error_list(error_list):
    return {
        'error_list': error_list,
    };

@register.inclusion_tag('lintory/show_vendor_list.html', takes_context=True)
def show_vendor_list(context, object_list):
    dict = defaults(context)
    dict['object_list'] = object_list
    return dict

@register.inclusion_tag('lintory/show_hardware_list.html', takes_context=True)
def show_hardware_list(context, object_list):
    dict = defaults(context)
    dict['object_list'] = object_list
    return dict

@register.inclusion_tag('lintory/show_location_list.html', takes_context=True)
def show_location_list(context, object_list):
    dict = defaults(context)
    dict['object_list'] = object_list
    return dict

@register.inclusion_tag('lintory/show_license_list.html', takes_context=True)
def show_license_list(context, object_list):
    dict = defaults(context)
    dict['object_list'] = object_list
    return dict

@register.inclusion_tag('lintory/show_license_key_list.html', takes_context=True)
def show_license_key_list(context, object_list):
    dict = defaults(context)
    dict['object_list'] = object_list
    return dict

@register.inclusion_tag('lintory/show_software_list.html', takes_context=True)
def show_software_list(context, object_list):
    dict = defaults(context)
    dict['object_list'] = object_list
    return dict

@register.inclusion_tag('lintory/show_software_installation_list.html', takes_context=True)
def show_software_installation_list(context, object_list):
    dict = defaults(context)
    dict['object_list'] = object_list
    return dict

@register.inclusion_tag('lintory/show_task_list.html', takes_context=True)
def show_task_list(context, object_list):
    dict = defaults(context)
    dict['object_list'] = object_list
    return dict

@register.inclusion_tag('lintory/show_hardware_task_list.html', takes_context=True)
def show_hardware_task_list(context, object_list):
    dict = defaults(context)
    dict['object_list'] = object_list
    return dict

@register.inclusion_tag('lintory/show_history.html', takes_context=True)
def show_history(context, type_id, object):
    dict = defaults(context)
    dict['type_id'] = type_id
    dict['object'] = object
    return dict

@register.inclusion_tag("lintory/show_license_key.html", takes_context=True)
def show_license_key(context, license_key):
    dict = defaults(context)
    dict['license_key'] = license_key
    return dict

@register.inclusion_tag('lintory/show_os_list.html', takes_context=True)
def show_os_list(context, object_list):
    dict = defaults(context)
    dict['object_list'] = object_list
    return dict

@register.inclusion_tag('lintory/show_data_list.html', takes_context=True)
def show_data_list(context, object_list):
    dict = defaults(context)
    dict['object_list'] = object_list
    return dict

@register.inclusion_tag('lintory/show_breadcrumbs.html')
def show_breadcrumbs(breadcrumbs):
        return {'breadcrumbs': breadcrumbs[:-1], 'object': breadcrumbs[-1] };


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
        if owner is None:
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

        if owner is None:
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

        if owner is None:
            software_installations = models.software_installation.objects.filter(
                    Q(active=True,software=software,license_key__isnull=False,license_key__license__owner__isnull=True) |
                    Q(active=True,software=software,license_key__isnull=True))
        else:
            software_installations = models.software_installation.objects.filter(
                    Q(active=True,software=software,license_key__license__owner=owner) |
                    Q(active=True,software=software,license_key__isnull=True))

        context[tag] = software_installations
        return ''


@register.tag
def get_permissions_from_type(parser, token):
    try:
        tag_name, add_tag, edit_tag, delete_tag, user, type = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly four arguments" % token.contents.split()[0]
    return get_permissions_from_type_node(add_tag, edit_tag, delete_tag, user, type)

class get_permissions_from_type_node(template.Node):
    def __init__(self, add_tag, edit_tag, delete_tag, user, type):
        self.add_tag = template.Variable(add_tag)
        self.edit_tag = template.Variable(edit_tag)
        self.delete_tag = template.Variable(delete_tag)
        self.user = template.Variable(user)
        self.type = template.Variable(type)
    def render(self, context):
        add_tag = self.add_tag.resolve(context)
        edit_tag = self.edit_tag.resolve(context)
        delete_tag = self.delete_tag.resolve(context)
        user = self.user.resolve(context)
        type = self.type.resolve(context)

        context[add_tag] = type.has_add_perms(user)
        context[edit_tag] = type.has_edit_perms(user)
        context[delete_tag] = type.has_delete_perms(user)
        return ''

def _get_link(i):
    return u"?page=%d"%(i)

@register.simple_tag
def paginator_prev(page_obj):
    if page_obj.number <= 1:
        return mark_safe(u'')
    else:
        return mark_safe(u"<a href='%s'>&lt;</a>" % (_get_link(page_obj.number-1)))

@register.simple_tag
def paginator_next(page_obj):
    if page_obj.number >= page_obj.paginator.num_pages:
        return mark_safe(u'')
    else:
        return mark_safe(u"<a href='%s'>&gt;</a>" % (_get_link(page_obj.number+1)))

@register.simple_tag
def paginator_number(page_obj,i):
    if i == DOT:
        return mark_safe(u'... ')
    elif i == page_obj.number:
        return mark_safe(u'<span class="this-page">%d</span> ' % (i))
    else:
        return mark_safe(u'<a href="%s"%s>%d</a> ' % (_get_link(i), (i == page_obj.paginator.num_pages and ' class="end"' or ''), i))

DOT='.'

@register.inclusion_tag('lintory/pagination.html')
def pagination(page_obj):
    paginator, page_num = page_obj.paginator, page_obj.number

    if paginator.num_pages <= 1:
        pagination_required = False
        page_range = []
    else:
        pagination_required = True
        ON_EACH_SIDE = 3
        ON_ENDS = 2

        # If there are 10 or fewer pages, display links to every page.
        # Otherwise, do some fancy
        if paginator.num_pages <= 10:
            page_range = range(1,paginator.num_pages+1)
        else:
            # Insert "smart" pagination links, so that there are always ON_ENDS
            # links at either end of the list of pages, and there are always
            # ON_EACH_SIDE links at either end of the "current page" link.
            page_range = []
            if page_num > (ON_EACH_SIDE + ON_ENDS + 1):
                page_range.extend(range(1, ON_ENDS+1))
                page_range.append(DOT)
                page_range.extend(range(page_num - ON_EACH_SIDE, page_num))
            else:
                page_range.extend(range(1, page_num))

            if page_num < (paginator.num_pages - ON_EACH_SIDE - ON_ENDS):
                page_range.extend(range(page_num, page_num + ON_EACH_SIDE + 1))
                page_range.append(DOT)
                page_range.extend(range(paginator.num_pages - ON_ENDS + 1, paginator.num_pages + 1))
            else:
                page_range.extend(range(page_num, paginator.num_pages + 1))

    return {
        'pagination_required': pagination_required,
        'page_obj': page_obj,
        'page_range': page_range,
    }

