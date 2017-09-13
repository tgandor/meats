@if [%1]==[] goto :usage

netsh interface ip add dns %*

goto:eof

:usage
@echo Usage: %0 Interface DNS_IP [index=N]
@echo Adds static DNS server for "Interface"
@echo Remember to be admin.
