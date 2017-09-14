#!/bin/bash

if [ -z "$1" ] ; then
    echo Usage: $0 NETWORK
    exit
fi

network=$1

if [ ! -e /etc/ntp.conf ] ; then
    echo NTP is not installed
    sudo apt-get install ntp
fi

if grep $network /etc/ntp.conf ; then
    echo Probably already configured...
    exit
fi

# replace non-zero bytes with 255 in IP for network mask
mask=`echo $network | sed s/[1-9][0-9]*/255/g`

echo restrict $network mask $mask nomodify notrap | sudo tee -a /etc/ntp.conf
