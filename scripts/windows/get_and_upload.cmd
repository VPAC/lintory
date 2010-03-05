set LUTILS=\\server\utils

net use %LUTILS%
if errorlevel 1 exit /b 1
cscript %LUTILS%\lintory\get_lintory.vbs > %TEMP%\lintory.txt
if errorlevel 1 exit /b 1
%LUTILS%\lintory\curl -T %TEMP%\lintory.txt -H "Content-Type: text/plain" --cacert \\hq\utils\certificates\apac\cacert.pem -o %TEMP%\lintory.html https://hq.in.vpac.org/inventory/upload/windows/
if errorlevel 1 exit /b 1

rem net use %LUTILS% /d

rem pause
