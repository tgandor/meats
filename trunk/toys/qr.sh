#!/bin/bash

missing=""

if ! which qrencode >/dev/null ; then
	missing="qrencode"
fi

if ! which display >/dev/null ; then
	missing="$missing imagemagick"
fi

if [ -n "$missing" ] ; then
	echo "Missing packages: $missing"
	echo "Trying to install:"
	if ! sudo apt-get install $missing ; then
		echo Install failed
		exit
	fi
fi

for i in "$@"; do
	echo "Showing $i..."
	qrencode "$i"  -o -| display -resize 300x300% -
done
