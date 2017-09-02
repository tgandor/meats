@echo off
:: https://derekgusoff.wordpress.com/2012/09/05/run-hyper-v-and-virtualbox-on-the-same-machine/

bcdedit /set hypervisorlaunchtype auto

if ERRORLEVEL 1 (
echo HINT: You need to be admin to do this.
) else (
echo Hyper-V turned on. Remember to reboot.
)
