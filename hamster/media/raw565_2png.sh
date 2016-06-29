#!/bin/bash

# http://www.madox.net/blog/2011/06/06/converting-tofrom-rgb565-in-ubuntu-using-ffmpeg/

command=ffmpeg
if ! which ffmpeg &>/dev/null ; then
	if which avconv &>/dev/null ; then
		command=avconv
	else
		echo "ffmpeg nor avconv not found"
		exit
	fi
fi

$command -vcodec rawvideo -f rawvideo -pix_fmt rgb565 -s 320x240 -i $1 -f image2 -vcodec png $1.png

# other way round:
# ffmpeg -vcodec png -i image.png -vcodec rawvideo -f rawvideo -pix_fmt rgb565 image.raw
