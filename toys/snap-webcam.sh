#!/bin/bash
subdir=`date +'%Y-%m-%d_%H-%M-%S'`
mkdir $subdir
cd $subdir
device=`ls /dev/video? | head -n 1`
if [ -z $w ]; then w=1280; fi
if [ -z $h ]; then h=1024; fi
mplayer -vo jpeg -frames 15 -fps 15 -tv driver=v4l2:width=$w:height=$h:device=$device tv://
echo "Frames stored in $subdir"

