@echo off

if [%~1]==[] (
    echo Usage: %0 file_to_launch.py
    exit /b
)

FOR /F %%p IN ('where activate.bat') DO echo call %%p > %~n1.bat
:: using shift and %* seems not to work as it should:
echo python %~f1 %2 %3 %4 %5 %6 %7 %8 %9 >> %~n1.bat

