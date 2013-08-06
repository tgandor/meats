#!/bin/bash
subdir=`date +'%Y-%m-%d_%H-%M-%S'`
mkdir $subdir
cd $subdir
if [ -z $device ]; then device=`ls /dev/video? | head -n 1`; fi
if [ -z $w ]; then w=1280; fi
if [ -z $h ]; then h=1024; fi
if [ -z $fps ]; then fps=15; fi
if [ -z $num ]; then num=15; fi
mplayer -vo jpeg -frames $num -fps $fps -tv driver=v4l2:width=$w:height=$h:device=$device tv://
echo "Frames stored in $subdir"

