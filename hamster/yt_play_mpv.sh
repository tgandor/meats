#!/bin/bash

if which yt-dlp ; then
    downloader="yt-dlp -S res:720"
elif which youtube-dl ; then
    downloader="youtube-dl -f 720p"
else
    echo "No youtube-dl or yt-dlp."
    exit
fi

$downloader -g "$1" | ( read vid; read aud; mpv "$vid" --audio-file="$aud" --cache-secs=5 )
