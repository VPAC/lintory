Option Explicit

Function Base64Encode(sText)
    Dim oXML, oNode

    Set oXML = CreateObject("Msxml2.DOMDocument.3.0")
    Set oNode = oXML.CreateElement("base64")
    oNode.dataType = "bin.base64"
    oNode.nodeTypedValue =Stream_StringToBinary(sText)
    Base64Encode = oNode.text
    Set oNode = Nothing
    Set oXML = Nothing
End Function

Function Base64Decode(ByVal vCode)
    Dim oXML, oNode

    Set oXML = CreateObject("Msxml2.DOMDocument.3.0")
    Set oNode = oXML.CreateElement("base64")
    oNode.dataType = "bin.base64"
    oNode.text = vCode
    Base64Decode = Stream_BinaryToString(oNode.nodeTypedValue)
    Set oNode = Nothing
    Set oXML = Nothing
End Function

Function IsAscii(s)
    With New RegExp
      .Pattern = "[^\x00-\x7f]"  ' Use [^\x00-\xff] for US-ASCII
      IsAscii = Not .Test(s)
    End With
End Function

'Stream_StringToBinary Function
'2003 Antonin Foller, http://www.motobit.com
'Text - string parameter To convert To binary data
Function Stream_StringToBinary(Text)
  Const adTypeText = 2
  Const adTypeBinary = 1

  'Create Stream object
  Dim BinaryStream 'As New Stream
  Set BinaryStream = CreateObject("ADODB.Stream")

  'Specify stream type - we want To save text/string data.
  BinaryStream.Type = adTypeText

  'Specify charset For the source text (unicode) data.
  BinaryStream.CharSet = "us-ascii"

  'Open the stream And write text/string data To the object
  BinaryStream.Open
  BinaryStream.WriteText Text

  'Change stream type To binary
  BinaryStream.Position = 0
  BinaryStream.Type = adTypeBinary

  'Ignore first two bytes - sign of
  BinaryStream.Position = 0

  'Open the stream And get binary data from the object
  Stream_StringToBinary = BinaryStream.Read

  Set BinaryStream = Nothing
End Function


' ------------- START -----------------

Dim ComputerName, wmiServices

ComputerName = "."

Set wmiServices  = GetObject ( _
    "winmgmts:{impersonationLevel=Impersonate}!//" _
    & ComputerName)

Wscript.StdOut.WriteLine "# Lintory"
WScript.StdOut.WriteLine "Date:"&year(date)&"-"&month(date)&"-"&day(date)
WScript.StdOut.WriteLine "Time:"&hour(time)&":"&minute(time)&":"&second(time)

' ------------- COMPUTER -----------------

Dim col, obj, Prop

Set col = wmiServices.ExecQuery _
    ("Select * from Win32_ComputerSystem")

For Each obj in col
    Wscript.StdOut.WriteLine ""
    Wscript.StdOut.WriteLine "# ComputerSystem"
    WriteProperties obj
Next

Set col = wmiServices.ExecQuery _
    ("Select * from Win32_SystemEnclosure")

For Each obj in col
    Wscript.StdOut.WriteLine ""
    Wscript.StdOut.WriteLine "# SystemEnclosure"
    WriteProperties obj
Next

Set col = wmiServices.ExecQuery _
    ("Select * from Win32_BaseBoard")

For Each obj in col
    Wscript.StdOut.WriteLine ""
    Wscript.StdOut.WriteLine "# BaseBoard"
    WriteProperties obj
Next

Set col = wmiServices.ExecQuery _
    ("Select * from Win32_Processor")

For Each obj in col
    Wscript.StdOut.WriteLine ""
    Wscript.StdOut.WriteLine "# Processor"
    WriteProperties obj
Next

Set col = wmiServices.ExecQuery _
    ("Select * from Win32_OperatingSystem")

For Each obj in col
    Wscript.StdOut.WriteLine ""
    Wscript.StdOut.WriteLine "# OperatingSystem"
    WriteProperties obj
Next

' ------------- DISPLAY -----------------

Set col = wmiServices.ExecQuery _
    ("Select * from Win32_VideoController")

For Each obj in col
    Wscript.StdOut.WriteLine ""
    Wscript.StdOut.WriteLine "# VideoController"
    WriteProperties obj
Next

Set col = wmiServices.ExecQuery _
    ("Select * from Win32_DesktopMonitor")

For Each obj in col
    Wscript.StdOut.WriteLine ""
    Wscript.StdOut.WriteLine "# DesktopMonitor"
    WriteProperties obj
Next

' ------------- NETWORK ADAPTOR -----------------

dim colNic, objNic, colNicConfigs, objNicConfig

Set colNic = wmiServices.ExecQuery _
    ("Select * from Win32_NetworkAdapter")

For Each objNic in colNic
    Wscript.StdOut.WriteLine ""
    Wscript.StdOut.WriteLine "# NetworkAdapter"
    WriteProperties objNic

    Set colNicConfigs = wmiServices.ExecQuery _
      ("ASSOCIATORS OF " _
          & "{Win32_NetworkAdapter.DeviceID='" & _
      objNic.DeviceID & "'}" & _
      " WHERE AssocClass=Win32_NetworkAdapterSetting")
    For Each objNicConfig In colNicConfigs
        Wscript.StdOut.WriteLine "## NetworkAdapterConfig"
        WriteProperties objNicConfig
    Next

Next

' ------------- DRIVES -----------------

Dim wmiDiskDrives, wmiDiskDrive, wmiDiskPartitions, wmiDiskPartition, wmiLogicalDisks, wmiLogicalDisk
Dim query

Set col = wmiServices.ExecQuery _
    ("Select * from Win32_CDROMDrive")

For Each obj in col
    Wscript.StdOut.WriteLine ""
    Wscript.StdOut.WriteLine "# CDROMDrive"
    WriteProperties obj
Next

Set wmiDiskDrives =  wmiServices.ExecQuery ( _
    "SELECT * FROM Win32_DiskDrive")

For Each wmiDiskDrive In wmiDiskDrives
    Wscript.StdOut.WriteLine ""
    WScript.StdOut.WriteLine "# DiskDrive"
    WriteProperties wmiDiskDrive

    'Use the disk drive device id to
    ' find associated partition
    query = "ASSOCIATORS OF {Win32_DiskDrive.DeviceID='" _
        & wmiDiskDrive.DeviceID & "'} WHERE AssocClass = Win32_DiskDriveToDiskPartition"    
    Set wmiDiskPartitions = wmiServices.ExecQuery(query)

    For Each wmiDiskPartition In wmiDiskPartitions
        WScript.StdOut.WriteLine "## DiskPartition"
        WriteProperties wmiDiskPartition

        'Use partition device id to find logical disk
        Set wmiLogicalDisks = wmiServices.ExecQuery _
            ("ASSOCIATORS OF {Win32_DiskPartition.DeviceID='" _
             & wmiDiskPartition.DeviceID & "'} WHERE AssocClass = Win32_LogicalDiskToPartition") 

        For Each wmiLogicalDisk In wmiLogicalDisks
            WScript.StdOut.WriteLine "### LogicalDisk"
            WriteProperties wmiLogicalDisk
        Next
    Next
Next

' ------------- LICENSE -----------------

Const HKEY_LOCAL_MACHINE = &H80000002
Dim foundKeys
Dim iValues
Dim arrDPID
Dim strHTML
Dim arrSubKeys(5)
Dim oReg
Dim x
Dim DigitalProductID
Dim ProductName
foundKeys = Array()
iValues = Array()
arrSubKeys(0) = "SOFTWARE\Microsoft\Windows NT\CurrentVersion"
arrSubKeys(2) = "SOFTWARE\Microsoft\Office\10.0\Registration"
arrSubKeys(1) = "SOFTWARE\Microsoft\Office\11.0\Registration"
arrSubKeys(3) = "SOFTWARE\Microsoft\Office\12.0\Registration"
arrSubKeys(4) = "SOFTWARE\Microsoft\Exchange\Setup"
arrSubKeys(5) = "SOFTWARE\Microsoft\Office\9.0\Registration"

' Open Registry Key and populate binary data into an array
Set oReg=GetObject("winmgmts:{impersonationLevel=impersonate}!\\" & ComputerName & "\root\default:StdRegProv")
For x = LBound(arrSubKeys, 1) To UBound(arrSubKeys, 1)
  oReg.GetBinaryValue HKEY_LOCAL_MACHINE, arrSubKeys(x), "DigitalProductID", DigitalProductID
  oReg.GetStringValue HKEY_LOCAL_MACHINE, arrSubKeys(x), "ProductName", ProductName

  If Not IsNull(DigitalProductID) Then
   call decodeKey(DigitalProductID, ProductName)
  Else
   Dim arrGUIDKeys, GUIDKey
   oReg.EnumKey HKEY_LOCAL_MACHINE, arrSubKeys(x), arrGUIDKeys
   If Not IsNull(arrGUIDKeys) Then
    For Each GUIDKey In arrGUIDKeys
     oReg.GetBinaryValue HKEY_LOCAL_MACHINE, arrSubKeys(x) & "\" & GUIDKey, "DigitalProductID", DigitalProductID
     oReg.GetStringValue HKEY_LOCAL_MACHINE, arrSubKeys(x) & "\" & GUIDKey, "ProductName", ProductName
     If Not IsNull(DigitalProductID) Then
       call decodeKey(DigitalProductID, ProductName)
     End If
    Next
  End If
End If
Next

' Return the Product Key
Function decodeKey(iValues, strProduct)
  Dim arrDPID
  Dim i, j, k, strProductKey
  arrDPID = Array()
  ' extract bytes 52-66 of the DPID
  For i = 52 to 66
    ReDim Preserve arrDPID( UBound(arrDPID) + 1 )
    arrDPID( UBound(arrDPID) ) = iValues(i)
  Next
  ' Create an array to hold the valid characters for a microsoft Product Key
  Dim arrChars
  arrChars = Array("B","C","D","F","G","H","J","K","M","P","Q","R","T","V","W","X","Y","2","3","4","6","7","8","9")
  ' The clever bit !!! (decode the base24 encoded binary data)
  For i = 24 To 0 Step -1
  k = 0
    For j = 14 To 0 Step -1
      k = k * 256 Xor arrDPID(j)
      arrDPID(j) = Int(k / 24)
      k = k Mod 24
    Next
    strProductKey = arrChars(k) & strProductKey
    If i Mod 5 = 0 And i <> 0 Then strProductKey = "-" & strProductKey
  Next
  ReDim Preserve foundKeys( UBound(foundKeys) + 1 )
  foundKeys( UBound(foundKeys) ) = strProductKey
  Wscript.StdOut.WriteLine ""
  Wscript.StdOut.WriteLine "# license key"
  Wscript.StdOut.WriteLine "Name: " & strProduct
  Wscript.StdOut.WriteLine "Product Key: " & strProductKey
End Function

' ------------- SOFTWARE -----------------

Dim colSoftware, objSoftware
Set colSoftware = wmiServices.ExecQuery _
    ("Select * from Win32_Product")

For Each objSoftware in colSoftware
    Wscript.StdOut.WriteLine ""
    Wscript.StdOut.WriteLine "# Product"
    WriteProperties objSoftware
Next

Wscript.StdOut.WriteLine ""
Wscript.StdOut.WriteLine "# end"

Sub WriteProperties(obj)

    For each Prop in obj.Properties_
        WScript.StdOut.Write Prop.Name & ": "
        If isArray(Prop.Value) Then
            Dim sep, value
            sep = ""
            For each value in Prop.Value
                WScript.StdOut.Write sep & Value
                sep = ","
            Next
        Elseif isNull(Prop.Value) Then
            WScript.StdOut.Write ""
        Elseif TypeName(Prop.Value) <> "String" Then
            WScript.StdOut.Write Prop.Value
        Elseif isAscii(Prop.Value) Then
            WScript.StdOut.Write Prop.Value
        Else
            WScript.StdOut.Write Base64Encode(Prop.Value)
        End If
        WScript.StdOut.WriteLine
    Next

end Sub
