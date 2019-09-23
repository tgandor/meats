#!/bin/bash

# not crediting anyone for the piping; everything I found didn't work.

# Other credits:
# -qscale:v - https://stackoverflow.com/a/10234065/1338797

out_dir=`date +%Y%m%d-%H%M%S`-ffmpeg
echo --------------------
echo Saving to: $out_dir
echo --------------------

mkdir -p $out_dir
# good to pass '-c:v copy' after the MJPEG URL
# ffmpeg -i "$@" $out_dir/ime_%06d.jpg -c:v copy -f mjpeg - | ffplay -f mjpeg  -i -
ffmpeg -i "$@" -qscale:v 2 $out_dir/ime_%06d.jpg -c:v copy -f matroska  - | ffplay -i -
