#!/bin/bash

# https://obrienlabs.net/raspberry-pi-spoof-mac-address/

if grep -q smsc95xx.macaddr /boot/cmdline.txt ; then
    echo Your MAC is already spoofed in /boot/cmdline.txt:
    grep -o 'smsc95xx.macaddr=[0-9A-Fa-f:]*' /boot/cmdline.txt
else
    echo No MAC spoofing found in /boot/cmdline.txt.
fi 

if [ -z "$1" ] ; then
    echo Usage: $0 MA:CA:DD:RE:SS
else
    echo Append this to /boot/cmdline.txt:
    echo smsc95xx.macaddr=$1
fi
