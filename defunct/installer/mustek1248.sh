#!/bin/bash

if [ -f /usr/share/sane/gt68xx/SBSfw.usb ] ; then
	echo Scanner already installed.
	exit
fi


if [ ! -d /usr/share/sane ]; then
	sudo apt-get install sane sane-utils python-imaging-sane
fi

if [ ! -d /usr/share/sane/gt68xx ]; then
	echo Missing gt68xx directory, creating...
	sudo mkdir -p /usr/share/sane/gt68xx
fi

if [ -f ~/SBSfw.usb ] ; then
	echo Installing firmware from home directory...
	sudo cp ~/SBSfw.usb /usr/share/sane/gt68xx
else
	echo Trying to download firmware...
	cd /usr/share/sane/gt68xx
	sudo wget http://www.meier-geinitz.de/sane/gt68xx-backend/firmware/SBSfw.usb
fi
