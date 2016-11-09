@echo off

:loop
if [%1]==[] goto :done
echo %1
shift
goto :loop

:done
echo Done.
