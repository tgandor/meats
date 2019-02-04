@echo off

:: thanks to: http://stackoverflow.com/a/14729312/1338797
:: see also: http://ss64.com/vb/syntax-elevate.html

REM Quick test for Windows generation: UAC aware or not ; all OS before NT4 ignored for simplicity
SET NewOSWith_UAC=YES
VER | FINDSTR /IL "5." > NUL
IF %ERRORLEVEL% == 0 SET NewOSWith_UAC=NO
VER | FINDSTR /IL "4." > NUL
IF %ERRORLEVEL% == 0 SET NewOSWith_UAC=NO


REM Test if Admin
CALL NET SESSION >nul 2>&1
IF NOT %ERRORLEVEL% == 0 (

    if /i "%NewOSWith_UAC%"=="YES" (
        rem Start batch again with UAC
        set UAC_ELEVATION=1
        echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
        echo UAC.ShellExecute "%~s0", "elevated", "", "runas", 1 >> "%temp%\getadmin.vbs"
        :: type "%temp%\getadmin.vbs"
        :: pause
        "%temp%\getadmin.vbs"
        del "%temp%\getadmin.vbs"
        set UAC_ELEVATION=
        exit /B
    )

    echo You have an old OS, without UAC.
    echo Some commands below will probably not work anyway.
)

rem Now we're in C:\Windows\System32
rem Use: cd %~dp0 if that's a problem.

@echo on

openfiles
@echo ERRORLEVEL %ERRORLEVEL%
net session
@echo ERRORLEVEL %ERRORLEVEL%

@echo.
@echo Some say this is the ultimate, best test:
fsutil dirty query %systemdrive%
@echo ERRORLEVEL %ERRORLEVEL%

@echo off
echo.

rem Recognizing the elevation source via the argument
if not "%1"=="elevated" goto :no_elev

echo We were elevated via VBS
    if defined UAC_ELEVATION (
        echo Parent environment accessible: UAC_ELEVATION=%UAC_ELEVATION%
    ) else (
        echo Parent environment not defined
    )
    pause
goto:eof
:no_elev
    echo No elevation via VBS was necessary
