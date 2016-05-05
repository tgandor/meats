@echo off

if "%1"=="" goto :help

findstr /S /R "%1" *
goto:eof

:help
echo Usage: wcgrep[.bat] PATTERN
