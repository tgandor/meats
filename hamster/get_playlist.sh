#!/bin/bash

if which youtube-dl >/dev/null 2>&1; then
    dl=youtube-dl
elif which yt-dlp >/dev/null 2>&1; then
    dl=yt-dlp
else
    echo "Neither youtube-dl nor yt-dlp found, please install one of them first."
    exit 1
fi

# .%(ext)s required because of -x, error otherwise.
# would like to --embed-thumbnail, but it only works for mp3 and m4a (not opus)
$dl -x --write-thumbnail -o "%(playlist_index)02d-%(title)s.%(ext)s" "$@"
