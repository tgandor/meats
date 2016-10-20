@echo off

if "%1"=="" goto :help

:: /S - search recursively through directories
:: /R - regex
:: /P - only files with printable characters ("text files")
:: /L - literal pattern (not regex)
:: /V - (grep -v) negate selection

findstr /S /R /P "%1" * | findstr /L /V ".git\\"
goto:eof

:help
echo Usage: wcgrep[.bat] PATTERN
