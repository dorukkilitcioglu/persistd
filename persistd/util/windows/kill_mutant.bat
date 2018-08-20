@echo off
rem https://superuser.com/questions/963183/multiple-sublime-instances-using-different-windows-credentials
rem Just in case this is run multiple times from a command line
set pid=
set handle=
set process_name=%PERSISTD_MUTANT_PROCESS_NAME%
set object_name=%PERSISTD_MUTANT_OBJECT_NAME%
rem Make the working directory the directory of the batch file
cd /d %~dp0
rem Find PID and Handle
for /f "tokens=3,6" %%i in ('handle\handle -p %process_name% -a %object_name% -accepteula ^| find "Mutant"') do set pid=%%i & set handle=%%j
if "%pid%"=="" exit
rem Close the handle
handle\handle -c %handle:~0,-1% -p %pid% -y > nul
