@echo off

if "%~1"=="" (
    echo Usage: %0 file.exe
    exit /b
)

:: find newest VS tools

set BEST_TOOLS=none
for /F "usebackq tokens=1,2 delims==" %%x in (`set vs`) do (
    echo %%x | findstr "TOOLS" >nul && set BEST_TOOLS=%%y
)

if "%BEST_TOOLS%"=="none" (
    echo No VS tools found.
    exit /b
)

:: echo Best tools found %BEST_TOOLS%

"%BEST_TOOLS%..\..\VC\bin\dumpbin.exe" /headers "%*" | findstr "machine"
