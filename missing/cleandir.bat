@echo off

:: http://stackoverflow.com/a/1502935/1338797

set destination=%1
if [%1]==[] set destination=.

del /q %destination%\*
for /d %%x in (%destination%\*) do rd /s /q "%%x"

