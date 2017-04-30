#!/bin/bash

# credits to: http://ninedegreesbelow.com/photography/exiftool-commands.html#rename

if [ -z "$1" ]; then
	echo "Usage: $0 IMAGE_FILE..."
	exit
fi

if ! which exiftool >/dev/null ; then
	sudo apt install libimage-exiftool-perl
fi

exiftool '-filename<CreateDate' -d %y%m%d_%H%M%S%%-c.%%le "$@"
