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

from django.db import models
import lintory

class char_field(models.CharField):

    def formfield(self, **kwargs):
        defaults = {'form_class': lintory.fields.char_field }
        defaults.update(kwargs)
        return super(char_field, self).formfield(**defaults)

class text_field(models.TextField):

    def formfield(self, **kwargs):
        defaults = {'form_class': lintory.fields.char_field }
        defaults.update(kwargs)
        return super(text_field, self).formfield(**defaults)

class email_field(models.EmailField):

    def formfield(self, **kwargs):
        defaults = {'form_class': lintory.fields.email_field }
        defaults.update(kwargs)
        return super(email_field, self).formfield(**defaults)

class mac_address_field(models.CharField):

    def __init__(self, *args, **kwargs):
        defaults = {'max_length': 17}
        defaults.update(kwargs)
        super(mac_address_field, self).__init__(**defaults)

    def formfield(self, **kwargs):
        defaults = {'form_class': lintory.fields.mac_address_field }
        defaults.update(kwargs)
        return super(mac_address_field, self).formfield(**defaults)
