#!/bin/bash

if which avconv ; then
	conv=avconv
else
	conv=ffmpeg
fi

if [ "$MP3" == "" ] ; then
    EXT=mp3
else
    EXT=$MP3
fi

for f in "$@"; do
	basename="${f%.*}"
	new_name=${basename}.$EXT
# this approach was limited:
# new_name=`echo $f | sed 's/.ogg$\|.m4a$\|.flv$\|.mp4$\|.opus$\|.mkv$/.mp3/'`
	if [ "$f" == "$new_name" ] ; then
		echo "$f - target same as source"
	else
		echo "$f -> $new_name"
		$conv -hide_banner -i "$f" -vn -y "`basename "$new_name"`" 2>&1
	fi
done
