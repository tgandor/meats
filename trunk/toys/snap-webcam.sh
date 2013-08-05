#!/bin/bash
subdir=`date +'%Y-%m-%d_%H-%M-%S'`
mkdir $subdir
cd $subdir
device=`ls /dev/video? | head -n 1`
mplayer -vo jpeg -frames 75 -fps 30 -tv driver=v4l2:width=1280:height=1024:device=$device tv://
echo "Frames stored in $subdir"

