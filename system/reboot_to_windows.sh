#!/bin/bash

# source:
# https://unix.stackexchange.com/questions/43196/how-can-i-tell-grub-i-want-to-reboot-into-windows-before-i-reboot

if ! grep GRUB_DEFAULT=saved /etc/default/grub ; then
    echo "Not configured"
    echo "Set GRUB_DEFAULT=saved in /etc/default/grub and then run:"
    echo "sudo grub-update"
    exit 1
fi

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

