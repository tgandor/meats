#!/bin/bash
if [ -z $device ]; then device=`ls /dev/video? | head -n 1`; fi
if [ -z $w ]; then w=1280; fi
if [ -z $h ]; then h=1024; fi
if [ -z $fps ]; then fps=30; fi
mplayer -fps $fps -tv driver=v4l2:width=$w:height=$h:device=$device tv://
