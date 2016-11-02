@echo off

rem Test if Admin
fsutil dirty query %systemdrive% >nul 2>nul

IF %ERRORLEVEL% == 0 goto :elevated
    rem Save working directory
    echo pushd "%cd%" > "%temp%\getadmin_cwd.bat"
    rem Prepare script 
    echo Set UAC = CreateObject^("Shell.Application"^) >> "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "%*", "%cd%", "runas", 1 >> "%temp%\getadmin.vbs"
    rem Execute - pops up new shell
    "%temp%\getadmin.vbs"
    rem Cleanup temporary file 1
    del "%temp%\getadmin.vbs"
    exit /B
:elevated

call %temp%\getadmin_cwd.bat
:: echo %*
%*
rem Cleanup temporary file 2
popd
del "%temp%\getadmin_cwd.bat"
pause
