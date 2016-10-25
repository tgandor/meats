#!/bin/bash

# Thanks to: http://6ftdan.com/allyourdev/2015/07/25/play-hd-youtube-from-the-raspberry-pi-command-line/

if [ -z "$1" ] ; then
	echo "Usage: $0 <URL|video_id>"
	exit
fi

omxplayer -o local `youtube-dl -g $1`

