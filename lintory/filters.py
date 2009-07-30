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

import filter

class party_filter(filter.ModelChoiceFilter):
    field_class = fields.party_field

class hardware_type_filter(filter.CharFilter):
    field_class = fields.hardware_type_field

class mac_address_filter(filter.CharFilter):
    field_class = fields.mac_address_field

class boolean_filter(filter.BooleanFilter):
    def filter(self, qs, value):
        lookup = self.lookup_type
        if value is not None:
            return qs.filter(**{'%s__%s' % (self.name, lookup): value})
        return qs

class inverted_boolean_filter(boolean_filter):
    field_class = filter.BooleanFilter.field_class

    def filter(self, qs, value):
        if value is not None:
            value = not value
        print value
        return super(inverted_boolean_filter,self).filter(qs, value)

class party(filter.FilterSet):
    name = filter.CharFilter(lookup_type='icontains')

    class Meta:
        model = models.party

class vendor(filter.FilterSet):
    name = filter.CharFilter(lookup_type='icontains')
    telephone = filter.CharFilter(lookup_type='icontains')
    email = filter.CharFilter(lookup_type='icontains')

    class Meta:
        model = models.vendor

class hardware(filter.FilterSet):
    type_id = hardware_type_filter(label="Type")
    computer = filter.CharFilter(name="computer__name",lookup_type='icontains')
    mac_address = mac_address_filter(name="network_adaptor__mac_address")
    manufacturer = filter.CharFilter(lookup_type='icontains')
    model = filter.CharFilter(lookup_type='icontains')
    serial_number = filter.CharFilter(lookup_type='icontains')
    asset_id = filter.CharFilter(lookup_type='icontains')
    owner = party_filter()
    user = party_filter()

    class Meta:
        model = models.hardware
        fields = [ 'location', 'installed_on' ]

class software(filter.FilterSet):
    name = filter.CharFilter(lookup_type='icontains')

    class Meta:
        model = models.software

class license(filter.FilterSet):
    owner = party_filter()

    class Meta:
        model = models.license

class task(filter.FilterSet):
    name = filter.CharFilter(lookup_type='icontains')
    comments = filter.CharFilter(lookup_type='icontains')

    class Meta:
        model = models.task

class data(filter.FilterSet):
    attempted = inverted_boolean_filter(lookup_type='isnull', name="last_attempt")
    last_attempt_after = filter.DateTimeFilter(lookup_type='gte', name="last_attempt")
    last_attempt_before = filter.DateTimeFilter(lookup_type='lt', name="last_attempt")
    datetime_after = filter.DateTimeFilter(lookup_type='gte', name="datetime")
    datetime_before = filter.DateTimeFilter(lookup_type='lt', name="datetime")
    imported = inverted_boolean_filter(lookup_type='isnull', name="imported")

    class Meta:
        model = models.data
        exclude = [ 'datetime', 'last_attempt' ]
