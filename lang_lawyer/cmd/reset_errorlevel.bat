@echo off
rem *** main ***

call :raise_error
echo After :raise_error ERRORLEVEL = %ERRORLEVEL%

call :empty
echo After :empty ERRORLEVEL = %ERRORLEVEL%

call :reset_error
echo After :reset_error ERRORLEVEL = %ERRORLEVEL%

:: this is needed at the end of the main body of the script
goto:eof

rem *** subroutines ***

:empty
goto:eof

:raise_error
exit /b 1

:reset_error
exit /b 0
