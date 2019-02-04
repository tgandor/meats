#!/bin/bash

# inspired by:
# http://hxcaine.com/blog/2013/02/28/running-gnuplot-as-a-live-graph-with-automatic-updates/

rm /tmp/power_now.dat

query_data() {
	for i in {1..60}  # 1 minute
	do
		awk 'BEGIN{FS="="} /POWER_NOW|CURRENT_NOW/ { print $2 / 1e6; }' /sys/class/power_supply/BAT0/uevent >> /tmp/power_now.dat
	sleep 1
	done
}

query_data &
sleep 2
gnuplot `dirname $0`/plot_battery.gnu
kill $!
