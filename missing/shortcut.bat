
:: from: https://superuser.com/a/836818/269542

@if [%1]==[] (
    @echo Usage: %0 SHORTCUT TARGET
    @goto:eof
)

set SHORTCUT='%1'
set TARGET='%~dpnx2'
set PWS=powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile

%PWS% -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut(%SHORTCUT%); $S.TargetPath = %TARGET%; $S.Save()"
