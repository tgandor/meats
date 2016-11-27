#!/bin/bash

if [ -z "$1" ]; then
	echo "Usage: $0 URL"
	exit
fi

# warm up sudo
sudo pwd > /dev/null

utcdate=`wget -S --spider $1 2>&1 | awk '/Date:/ { sub(" *Date: +", ""); print; exit }'`
echo "$utcdate"
sudo date -u -s "$utcdate"

