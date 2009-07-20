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

def strip_software_version(software_name):
    m = None

    if m is None:
        m = re.match("^(.*) Update (\d+)$", software_name)

    if m is None:
        m = re.match("^(7-Zip) (\d+\.\d+)$", software_name)

    if m is None:
        m = re.match("^(ActivePerl) (\d+\.\d+\.\d+ Build \d+)$", software_name)

    if m is None:
        m = re.match("^(ActivePython) (\d+\.\d+\.\d+ Build \d+)$", software_name)

    if m is None:
        m = re.match("^Adobe Acrobat (6\.0\.\d+) Standard$", software_name)
        if m is not None:
            return [ ("Adobe Acrobat 6.0 Standard",m.group(1)), ]

    if m is None:
        m = re.match("^Adobe Acrobat - Reader (6\.0\.\d+) Update$", software_name)
        if m is not None:
            return [ ("Adobe Acrobat 6.0 Standard",m.group(1)), 
                     ("Adobe Reader", m.group(1)) ]

    if m is None:
        m = re.match("^Adobe Acrobat and Reader (6\.0\.\d+) Update$", software_name)
        if m is not None:
            return [ ("Adobe Acrobat 6.0 Standard",m.group(1)), 
                     ("Adobe Reader", m.group(1)) ]

    if m is None:
        m = re.match("^(Adobe Reader) (\d+)$", software_name)

    if m is None:
        m = re.match("^(Adobe Reader) (\d+\.\d+)$", software_name)

    if m is None:
        m = re.match("^(Adobe Reader) (\d+\.\d+\.\d+)$", software_name)

    if m is None:
        m = re.match("^(Java Advanced Imaging) (\d+\.\d+\.\d+) for ([A-Z]+)$", software_name)

    if m is None:
        m = re.match("^(Java 2 SDK, SE) v(1\.4\.2_\d+)$", software_name)

    if m is None:
        m = re.match("^(Java 2 Runtime Environment, SE) v([\d\._]+)$", software_name)

    if m is None:
        m = re.match("^(LightScribe) +(\d+\.\d+\.\d+\.\d+)", software_name)

    if m is None:
        m = re.match("^(NUnit) (\d+\.\d+)$", software_name)

    if m is None:
        m = re.match("^(NUnit) (\d+\.\d+\.\d+)$", software_name)

    if m is None:
        m = re.match("^(Microsoft .NET Compact Framework \d+.\d+) SP(\d+) Developer$", software_name)

    if m is None:
        m = re.match("^(Microsoft .NET Compact Framework \d+.\d+) SP(\d+)$", software_name)

    if m is None:
        m = re.match("^(Microsoft .NET Framework \d+.\d+) Service Pack (\d+)$", software_name)

    if m is None:
        m = re.match("^(Microsoft .NET Framework \d+.\d+) SP(\d+)$", software_name)

    if m is None:
        m = re.match("^(Microsoft DirectX SDK) \(([A-Za-z0-9 ]+)\)$", software_name)

    if m is None:
        m = re.match("^(Microsoft IntelliPoint) (\d+\.\d+)$", software_name)

    if m is None:
        m = re.match("^(Microsoft IntelliType Pro) (\d+\.\d+)$", software_name)

    if m is None:
        m = re.match("^Microsoft Silverlight Tools for Visual Studio 2008 SP(\d+) - ENU$", software_name)
        if m is not None:
            return [ ("Microsoft Silverlight Tools for Visual Studio 2008 - ENU",m.group(1)), ]

    if m is None:
        m = re.match("^(Microsoft Virtual PC 2007) SP(\d+)$", software_name)

    if m is None:
        m = re.match("^(Microsoft Visual C\+\+ 2008 Redistributable - [A-Za-z0-9]+) ([\.\d]+)$", software_name)

    if m is None:
        m = re.match("^(MySQL Server) (\d+\.\d+)$", software_name)

    if m is None:
        m = re.match("^(OpenOffice.org) (\d+\.\d+)$", software_name)

    if m is None:
        m = re.match("^(MySQL Connector/ODBC) (\d+\.\d+)$", software_name)

    if m is None:
        m = re.match("^(MySQL Tools) for (\d+\.\d+)$", software_name)

    if m is None:
        m = re.match("^(MySQL Workbench) (\d+\.\d+) OSS$", software_name)

    if m is None:
        m = re.match("^(Python) (\d+\.\d+)$", software_name)

    if m is None:
        m = re.match("^(Python) (\d+\.\d+\.\d+)$", software_name)

    if m is None:
        m = re.match("^(SkypeT) (\d+\.\d+)$", software_name)

    if m is None:
        m = re.match("^(Rhinoceros 4.0) SR(\d+[a-z])$", software_name)

    if m is None:
        m = re.match("^(TortoiseSVN) (\d+\.\d+\.\d+\.\d+) \(32 bit\)$", software_name)

    if m is None:
        m = re.match("^(Visual C\+\+ 2008 [a-zA-Z0-9]+ Runtime) - \((v\d+\.\d+\.\d+)\)", software_name)

    if m is None:
        m = re.match("^(Windows Azure Tools for Microsoft Visual Studio 1.0 CTP) \((\d+/\d+/\d+)\)", software_name)

    if m is None:
        m = re.match("^(Windows Rights Management Client) with Service Pack (\d+)", software_name)

    if m is None:
        m = re.match("^(Windows Rights Management Client Backwards Compatibility) SP(\d+)", software_name)

    if m is not None:
        return [ (m.group(1),m.group(2)), ]

    return [ (software_name,None), ]

