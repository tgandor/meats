#!/bin/bash

# credits to: http://ninedegreesbelow.com/photography/exiftool-commands.html#rename

if [ -z "$1" ]; then
	echo "Usage: $0 IMAGE_FILE..."
	exit
fi

if ! which exiftool >/dev/null ; then
	sudo apt install libimage-exiftool-perl
fi

# only difference between 'normal' exif reaname is the field: DateTimeOriginal
# (instead of CreateDate)

exiftool '-filename<DateTimeOriginal' -d %Y%m%d_%H%M%S%%-c.%%le "$@"
