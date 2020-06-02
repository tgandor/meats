#!/bin/bash

if [ "$2" == "" ] ; then
    echo "Usage: $0 <video> <audio>"
    exit
fi

# https://superuser.com/questions/1137612/ffmpeg-replace-audio-in-video

echo "Trying to replace audio of $1 with $2 producing out_$1..."
ffmpeg -i "$1" -i "$2" -c copy -map 0:v:0 -map 1:a:0 "out_$1"

