#!/bin/bash
set -xe
# warning: application specific (quality...)

bname=`basename $1 .mp4`
rate=`ffprobe -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=r_frame_rate $1`
~/meats/media/video_to_images.py $1
~/meats/media/detect_subtitles.py -p "$bname/*.png"
~/meats/media/images_to_mp4.py -nv -q 29 -r $rate -o "img_$bname.mp4" "$bname/*.png"
rm -r $bname
~/meats/media/replace_audio_in_video.sh "img_$bname.mp4" $1
rm "img_$bname.mp4"
