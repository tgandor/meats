#!/bin/bash

# https://stackoverflow.com/a/70816994/1338797
# ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames -print_format csv="p=0" "$1"
# ffprobe -i "$1" -show_entries format=duration -v quiet -of csv="p=0"
# echo $(( $frames / $duration))

# Not really, so check other answer:

ffprobe -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=r_frame_rate "$1" | while read rate ; do
    echo $rate
    python -c "print($rate)"
done

