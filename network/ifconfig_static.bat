@if [%2]==[] goto :usage

netsh interface ip set address %1 static %2 255.255.255.0 %3

goto:eof

:usage
@echo Usage: %0 Interface IP_address [Gateway]
@echo Sets "Interface" to static IP address [not alternative].
@echo Optionally specify 3rd argument for default gateway.
@echo Remember to be admin.
