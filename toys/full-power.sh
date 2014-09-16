#!/bin/bash

if [ "$1" = "off" ]; then
	governor=ondemand
elif [ "$1" = "down" ]; then
	governor=powersave
else
	governor=performance
fi

if [ "$1" != "show" -a "$1" != "list" ] ; then
	echo "Activating $governor governor..."
	# sudo cpufreq-set -r -g $governor
	echo $governor | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor > /dev/null
fi

echo "Checking:"
head /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor 
