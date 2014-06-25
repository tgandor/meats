#!/bin/bash

if [ "$1" == "off" ]; then
	echo "Activating ondemand governor..."
	# sudo cpufreq-set -r -g ondemand
	echo ondemand | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor > /dev/null
else
	echo "Activating performance governor..."
	# sudo cpufreq-set -r -g performance
	echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor > /dev/null
fi
