#!/bin/bash

if [ -z "$1" ]; then
	echo "Usage: $0 [-s] URL"
	exit
fi


if [ "$2" == "-s" ]; then
	# warm up sudo
	sudo pwd > /dev/null
	elevate=sudo
	switch="-u -s"
else
	elevate=""
	switch="-d"
fi

utcdate=`wget -S --spider $1 2>&1 | awk '/Date:/ { sub(" *Date: +", ""); print; exit }'`

echo "Local: "`date`
$elevate date $switch "$utcdate"
