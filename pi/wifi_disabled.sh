#!/bin/bash

if grep dtoverlay=pi3-disable-wifi /boot/config.txt ; then
    echo WiFi is manually disabled in /boot/config.txt
else
    echo WiFi should be on, if this is Pi3
fi

