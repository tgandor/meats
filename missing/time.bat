@echo off

if "%1"=="" (
echo Usage: %0 command-to-measure [args...]
exit /b
)

@setlocal
set start=%time%
call %*
echo.
call :print_time_since %start%
@endlocal
goto:eof

:: auxiliary function, based on:
:: http://stackoverflow.com/questions/673523/how-to-measure-execution-time-of-command-in-windows-command-line

:print_time_since
@setlocal
	:: if we called with "%start_variable%" (quoted)
	:: set start=%~1

	:: this does the trick for non-quoted version
	set start=%*

	:: until now:
	set end=%time%

	:: echo %start% vs %end%

	set options="tokens=1-4 delims=:.,"

	for /f %options% %%a in ("%start%") do set start_h=%%a&set /a start_m=100%%b %% 100&set /a start_s=100%%c %% 100&set /a start_ms=100%%d %% 100
	for /f %options% %%a in ("%end%") do set end_h=%%a&set /a end_m=100%%b %% 100&set /a end_s=100%%c %% 100&set /a end_ms=100%%d %% 100

	:: echo %end_h%-%start_h%
	:: echo %end_m%-%start_m%
	:: echo %end_s%-%start_s%
	:: echo %end_ms%-%start_ms%

	set /a hours=%end_h%-%start_h%
	set /a mins=%end_m%-%start_m%
	set /a secs=%end_s%-%start_s%
	set /a ms=%end_ms%-%start_ms%

	:: carry, for differences < 0
	if %hours% lss 0 set /a hours = 24%hours%
	if %mins% lss 0 set /a hours = %hours% - 1 & set /a mins = 60%mins%
	if %secs% lss 0 set /a mins = %mins% - 1 & set /a secs = 60%secs%
	if %ms% lss 0 set /a secs = %secs% - 1 & set /a ms = 100%ms%
	
	:: mission accomplished
	set /a totalsecs = %hours%*3600 + %mins%*60 + %secs% 
	
	:: zero padding - note: must be after computing the totalsecs variable
	if 1%ms% lss 100 set ms=0%ms%
	if %hours% lss 10 set hours=0%hours%
	if %mins% lss 10 set mins=0%mins%
	if %secs% lss 10 set secs=0%secs%
	
	echo %hours%:%mins%:%secs%.%ms% elapsed (%totalsecs%.%ms%s total)
@endlocal
goto:eof