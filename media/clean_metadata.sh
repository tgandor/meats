#!/bin/bash

mkdir -p clean
for i in "$@"; do
    ffmpeg -hide_banner -i "$i" -c copy -map 0 -map_metadata 0:s:0 "clean/$(basename "$i")"
done
