#!/bin/bash

if which avconv ; then 
	conv=avconv
else
	conv=ffmpeg
fi

for f in "$@"; do
	basename="${f%.*}"
	new_name=${basename}.mp3
# this approach was limited:
# new_name=`echo $f | sed 's/.ogg$\|.m4a$\|.flv$\|.mp4$\|.opus$\|.mkv$/.mp3/'`
	if [ "$f" == "$new_name" ] ; then
		echo "$f - target same as source"
	else
		echo "$f -> $new_name"
		$conv -i "$f" -vn -y "`basename "$new_name"`" 2>&1
	fi
done
