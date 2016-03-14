#!/bin/bash

missing=""
if ! which scanimage >/dev/null ; then
	missing="sane-utils"
fi
if ! which lpr >/dev/null ; then
	missing="$missing cups-bsd"
fi
if ! which mogrify >/dev/null; then
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

if [ "$1" == "-s" ] ; then
	if [ -n "$2" ] ; then
		extra="_$2"
	fi
	tmpdf=`date +"%Y-%m-%d_%H-%M-%S"`$extra.tif
	title=$tmpdf
	
else
	tmpdf=/tmp/photocopy.tif
	title=Photocopy
fi

echo "Scanning to: $tmpdf"

scanimage -p --format=tiff > $tmpdf
if [ "$1"=="-e" -o "$2"=="-e" -o "$3"=="-e" ] ; then
	# leaving all modifications to the user
	gimp $tmpdf
else
	# shaving and thresholding may be scanner-specific
	mogrify -level-colors "gray(35%),gray(85%)" -shave 80x30-80-30 $tmpdf
	lpr -T $title $tmpdf
fi
