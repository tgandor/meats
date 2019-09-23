#!/bin/bash

# http://www.madox.net/blog/2011/06/06/converting-tofrom-rgb565-in-ubuntu-using-ffmpeg/
# http://wiki.bash-hackers.org/howto/getopts_tutorial

command=ffmpeg
if ! which ffmpeg &>/dev/null ; then
	if which avconv &>/dev/null ; then
		command=avconv
	else
		echo "ffmpeg nor avconv not found"
		exit
	fi
fi

while getopts d opt; do
	case $opt in
		d)
			delete=1
			;;
		\?)
			;;
	esac
done

# consume options
shift $((OPTIND-1))

for f in "$@"; do
	$command -vcodec rawvideo -f rawvideo -pix_fmt rgb565 -s 320x240 -i "$f" -f image2 -vcodec png "$f.png"
	if [ $? -eq 0 ] && [ -n  "$delete" ]; then
		echo "deleting $f ..."
		rm "$f"
	fi
done

# other way round:
# ffmpeg -vcodec png -i image.png -vcodec rawvideo -f rawvideo -pix_fmt rgb565 image.raw
