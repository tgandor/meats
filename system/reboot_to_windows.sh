#!/bin/bash

# source:
# https://unix.stackexchange.com/questions/43196/how-can-i-tell-grub-i-want-to-reboot-into-windows-before-i-reboot

grep GRUB_DEFAULT=saved /etc/default/grub || ( echo "Not configured" ; exit 1 )

WINDOWS_TITLE=`grep -i "^menuentry 'Windows" /boot/grub/grub.cfg|head -n 1|cut -d"'" -f2`

echo "Windows entry: $WINDOWS_TITLE"

sudo grub-reboot "$WINDOWS_TITLE"

echo "Checking settings:"
sudo grub-editenv list 

if [ "$1"=="now" ] ; then
    sudo reboot
else
    echo "Probably you can now reboot"
fi

