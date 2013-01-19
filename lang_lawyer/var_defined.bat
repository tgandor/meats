@echo off
:: what does this illustrate?
:: well, first - the definedness of a variable:
:: setting it to nothing makes it not defined
:: secondly - here's how to use subroutines ;)
:: more than one subroutine? use goto :eof as return

call :check
set xxx=abc
call :check
set xxx=
call :check
pause
exit

:check
if defined xxx echo "defined"
if not defined xxx echo "not defined"
