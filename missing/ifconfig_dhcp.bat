@if [%1]==[] goto :usage

netsh interface ip set address %1 dhcp
netsh interface ip set dnsservers %1 dhcp

goto:eof

:usage
@echo Usage: %0 Interface
@echo Resets "Interface" to DHCP address and DNS servers.
@echo Remember to be admin.
