#!/bin/bash

# credits to: http://ninedegreesbelow.com/photography/exiftool-commands.html#rename

if [ -z "$1" ]; then
	echo "Usage: $0 IMAGE_FILE..."
	exit
fi

exiftool '-filename<CreateDate' -d %y%m%d_%H%M%S%%-c.%%le "$@"
