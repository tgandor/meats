#!/bin/bash

# warning: application specific... (framerate, quality...)

bname=`basename $1 .mp4`
~/meats/media/video_to_images.py $1
~/meats/media/detect_subtitles.py -p "$bname/*.png"
~/meats/media/images_to_mp4.py -nv -q 29 -r 23.976024 -o "img_$bname.mp4" "$bname/*.png"
rm -r $bname
~/meats/media/replace_audio_in_video.sh "img_$bname.mp4" $1
rm "img_$bname.mp4"
