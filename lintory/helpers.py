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

from lintory.models import *

class invalid_mac_address(Exception):
        def __init__(self, value):
                self.value = value

        def __unicode__(self):
                return repr(self.value)

def fix_mac_address(ethernet_address):
        r = ethernet_address.upper();

        g = "[A-F0-9][A-F0-9]";
        m = re.match("^(%s):(%s):(%s):(%s):(%s):(%s)$"
                     %(g,g,g,g,g,g),r)
        if m is not None:
                return r

        m = re.match("^(%s)-(%s)-(%s)-(%s)-(%s)-(%s)$"
                     %(g,g,g,g,g,g),r)
        if m is None:
                raise invalid_mac_address("Cannot parse %s"%(r))

        r = "%s:%s:%s:%s:%s:%s" % (
                                m.group(1),
                                m.group(2),
                                m.group(3),
                                m.group(4),
                                m.group(5),
                                m.group(6))

        return r;

