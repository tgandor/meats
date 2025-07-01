#!/bin/bash

if which youtube-dl >/dev/null 2>&1; then
    dl=youtube-dl
elif which yt-dlp >/dev/null 2>&1; then
    dl=yt-dlp
else
    echo "Neither youtube-dl nor yt-dlp found, please install one of them first."
    exit 1
fi

# to consider: --write-info-json
$dl --extract-audio --audio-format mp3 --embed-thumbnail --output "%(playlist_index)02d-%(title)s.%(ext)s" "$@"
