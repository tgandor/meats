:: Sometimes you get downloading 0% forever
:: in the spirit of HYTTIOAOA?

:: This needs admin command prompt BTW.
:: https://answers.microsoft.com/en-us/windows/forum/windows_vista-update/windows-update-will-not-download-updates-stuck-at/3d4e2cff-d825-4271-9463-7ffb110c70f3
:: - sometimes stopping Windows Update is not enough.
:: most of C:\Windows\SoftwareDistribution will be deleted. but not all.

:: Next up:
:: https://answers.microsoft.com/en-us/windows/forum/all/windows-defender-update-stuck-on-0-downloading/fcf7d5d4-caa7-417c-b1fc-b82a813829c9

net stop bits
net stop wuauserv
net stop appidsvc
net stop cryptsvc

:: that's what they propose:
:: Ren %systemroot%\SoftwareDistribution SoftwareDistribution.bak
:: Ren %systemroot%\system32\catroot2 catroot2.bak

:: let's do it my way instead:
rmdir /q /s %systemroot%\SoftwareDistribution SoftwareDistribution.bak
rmdir /q /s %systemroot%\system32\catroot2 catroot2.bak

:: restart it back
:: caveat: maybe not all of this was running...

net start bits
net start wuauserv
net start appidsvc
net start cryptsvc

echo Now better reboot.
echo Maybe some services were started unnecessarily.

:: What about:
:: DISM.exe /Online /Cleanup-image /Scanhealth
:: and
:: DISM.exe /Online /Cleanup-image /Restorehealth
:: ?

:: Answer: maybe next time.
