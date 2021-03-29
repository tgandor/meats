@rem https://superuser.com/questions/19992/ipconfig-for-one-network-adaptor-only

@if [%1]==[-q] goto:short

netsh interface ip show addresses %*

goto:eof

:short
    @shift /1
    netsh interface ip show addresses %1 | findstr interface
