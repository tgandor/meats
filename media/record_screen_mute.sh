#!/bin/bash
output=`date +%Y%m%d-%H%M`_screen.mp4
ffmpeg -video_size 1920x1080 -framerate 25 -f x11grab -i :0.0+0,0 $output
