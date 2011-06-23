import re

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


def get_license_key(software_name, license_keys):
    key = None

    try:
        if software_name in license_keys:
            key = license_keys[software_name]

        elif software_name == "Microsoft Windows Server 2008 Standard":
            key = license_keys["Windows Server (R) 2008 Standard"]

        elif software_name == "Microsoft Windows Vista Business":
            key = license_keys["Windows Vista (TM) Business"]

        elif software_name == "Microsoft Windows Vista Ultimate":
            key = license_keys["Windows Vista (TM) Ultimate"]

        elif software_name == "Microsoft Windows XP Professional":
            key = license_keys["Microsoft Windows XP"]

        elif software_name == "Microsoft Windows 7 Home Premium":
            key = license_keys["Windows 7 Home Premium"]

        elif software_name == "Microsoft Windows 7 Professional":
            key = license_keys["Windows 7 Professional"]

        elif software_name == "Microsoft Windows 7 Ultimate":
            key = license_keys["Windows 7 Ultimate"]
    except KeyError, e:
        key = None

    return key
