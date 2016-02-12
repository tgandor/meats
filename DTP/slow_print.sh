#!/bin/bash

mkdir -p done

for i in "$@"; do
	echo "$i"
	lp "$i"
	sleep 1
	while lpq | grep active; do
		echo 'waiting...'
		sleep 1
	done
	mv "$i" done
	echo "Finished, sleeping..."
	sleep 3
done
