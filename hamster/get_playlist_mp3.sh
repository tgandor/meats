#!/bin/bash

if which youtube-dl >/dev/null 2>&1; then
    dl=youtube-dl
elif which yt-dlp >/dev/null 2>&1; then
    dl=yt-dlp
else
    echo "Neither youtube-dl nor yt-dlp found, please install one of them first."
    exit 1
fi

$dl --write-info-json --write-description --windows-filenames --extract-audio --audio-format mp3 --embed-thumbnail --output "%(playlist_index)02d-%(title)s.%(ext)s" "$@"

mkdir -p .meta
mv *.description .meta
if which jq >/dev/null 2>&1; then
    find -name "*.info.json" | while read ij ; do
	jq . "$ij" > ".meta/$ij"
        rm "$ij"
    done
else
    echo "Missing jq, no formatting of .info.json-s"
    mv *.info.json .meta
fi
