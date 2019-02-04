@echo off

set ARCH=x64
set DLL=mingw
set EXE=msvc

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

"%BEST_TOOLS%..\..\VC\bin\cl.exe"

if "%1"=="" (
    echo "BTW, usage: %0 [DLL(=mingw) [EXE](=msvc)]"
) else (
    set DLL=%1
    if NOT "%2"=="" (
        set EXE=%2
    )
)

where "g++.exe"
if ERRORLEVEL 1 (
    echo "Missing MinGW G++ Compiler"
    exit /b
)

if "%DLL%"=="mingw" (
    "g++.exe" -shared -o lib_orig.dll lib.cpp -Wl,--output-def,lib_orig.def,--out-implib,lib_orig.a
    copy lib_orig.dll lib.dll
)

echo ---------------------------------------

python ..\dll_to_lib.py lib.dll

if %ARCH%==x64 (
    call "%BEST_TOOLS%..\..\VC\vcvarsall.bat" amd64
) else (
    call "%BEST_TOOLS%vsvars32.bat"
)

lib /machine:%ARCH% /def:lib_orig.def

echo ---------------------------------------


if "%EXE%"=="msvc" (
    cl /Feorig_prog.exe prog.cpp lib_orig.lib
)

cl /Ferev_eng_prog.exe prog.cpp lib.lib

echo 16 | orig_prog.exe

echo 21 | rev_eng_prog.exe
