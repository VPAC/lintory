set LUTILS=\\server\utils

net use %LUTILS%
cscript %LUTILS%\lintory\get_lintory.vbs > %TEMP%\lintory.txt
%LUTILS%\lintory\curl -T %TEMP%\lintory.txt -H "Content-Type: text/plain" --cacert %LUTILS%\cacert.pem -o %TEMP%\lintory.html https://server.example.org/inventory/upload/windows/

rem net use %LUTILS% /d

rem pause
