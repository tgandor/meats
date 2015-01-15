#!/bin/bash

if ! (apt-cache policy | grep pepper-flash) ; then
	sudo apt-add-repository ppa:skunk/pepper-flash
else
	echo PPA already added
fi

if ! dpkg -l pepflashplugin-installer ; then
	sudo apt-get update
	sudo apt-get install pepflashplugin-installer
else
	echo pepflashplugin-installer already installed
fi

if ! grep pepper-flash /etc/chromium-browser/default ; then
	# . /usr/lib/pepflashplugin-installer/pepflashplayer.sh
	echo Missing . /usr/lib/pepflashplugin-installer/pepflashplayer.sh in /etc/chromium-browser/default 
	echo ". /usr/lib/pepflashplugin-installer/pepflashplayer.sh" | sudo tee -a /etc/chromium-browser/default 
else
	echo Your /etc/chromium-browser/default seems already configured.
fi

