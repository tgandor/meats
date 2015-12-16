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

tmpdf=/tmp/photocopy.tif
scanimage -p --format=tiff > $tmpdf
# shaving and thresholding may be scanner-specific
mogrify -level-colors "gray(35%),gray(85%)" -shave 80x30-80-30 $tmpdf
lpr -T "Photocopy" $tmpdf
# rm $tmpdf
