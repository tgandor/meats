#!/bin/bash
device=`ls /dev/video? | head -n 1`
if [ -z $w ]; then w=1280; fi
if [ -z $h ]; then h=1024; fi
mplayer -fps 30 -tv driver=v4l2:width=$w:height=$h:device=$device tv://
