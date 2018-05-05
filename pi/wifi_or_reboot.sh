#!/bin/bash

# inspired by: http://weworkweplay.com/play/rebooting-the-raspberry-pi-when-it-loses-wireless-connection-wifi/

if [ "$1"=="" ] ; then
	ip=192.168.1.1
else
	ip=$1
fi

ping -c4 $ip > /dev/null 

if [ $? != 0 ] ; then
	echo Rebooting due to network failure.
	sudo /sbin/reboot
fi

