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

from lintory import models, fields

import django_filters

class party_filter(django_filters.ModelChoiceFilter):
    field_class = fields.party_field

class hardware_type_filter(django_filters.CharFilter):
    field_class = fields.hardware_type_field

class mac_address_filter(django_filters.CharFilter):
    field_class = fields.mac_address_field

class boolean_filter(django_filters.BooleanFilter):
    def filter(self, qs, value):
        lookup = self.lookup_type
        if value is not None:
            return qs.filter(**{'%s__%s' % (self.name, lookup): value})
        return qs

class inverted_boolean_filter(boolean_filter):
    field_class = django_filters.BooleanFilter.field_class

    def filter(self, qs, value):
        if value is not None:
            value = not value
        return super(inverted_boolean_filter,self).filter(qs, value)

class party(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = models.party

class vendor(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type='icontains')
    telephone = django_filters.CharFilter(lookup_type='icontains')
    email = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = models.vendor

class hardware(django_filters.FilterSet):
    type_id = hardware_type_filter(label="Type")
    computer = django_filters.CharFilter(name="computer__name",lookup_type='icontains')
    is_installed = inverted_boolean_filter(lookup_type='isnull', name="installed_on")
    mac_address = mac_address_filter(name="network_adaptor__mac_address")
    manufacturer = django_filters.CharFilter(lookup_type='icontains')
    model = django_filters.CharFilter(lookup_type='icontains')
    serial_number = django_filters.CharFilter(lookup_type='icontains')
    asset_id = django_filters.CharFilter(lookup_type='icontains')
    owner = party_filter()
    user = party_filter()

    class Meta:
        model = models.hardware
        fields = [ 'location', 'installed_on' ]

class software(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type='icontains')
    has_licenses = inverted_boolean_filter(lookup_type='isnull', name="license_key")

    class Meta:
        model = models.software

class license(django_filters.FilterSet):
    owner = party_filter()

    class Meta:
        model = models.license

class task(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type='icontains')
    comments = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = models.task

class data(django_filters.FilterSet):
    attempted = inverted_boolean_filter(lookup_type='isnull', name="last_attempt")
    last_attempt_after = django_filters.DateTimeFilter(lookup_type='gte', name="last_attempt")
    last_attempt_before = django_filters.DateTimeFilter(lookup_type='lt', name="last_attempt")
    datetime_after = django_filters.DateTimeFilter(lookup_type='gte', name="datetime")
    datetime_before = django_filters.DateTimeFilter(lookup_type='lt', name="datetime")
    imported = inverted_boolean_filter(lookup_type='isnull', name="imported")

    class Meta:
        model = models.data
        exclude = [ 'datetime', 'last_attempt' ]
