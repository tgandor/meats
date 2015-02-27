#!/bin/bash
if [ -z $device ]
  then device=`ls /dev/video? | head -n 1`
elif [ $device == 0 ]
  then device=/dev/video0
elif [ $device == 1 ]
  then device=/dev/video1
elif [ $device == 2 ]
  then device=/dev/video2
fi
if [ -z $w ]; then w=1280; fi
if [ -z $h ]; then h=720; fi
if [ -z $fps ]; then fps=30; fi
mplayer -fps $fps -vf screenshot -tv driver=v4l2:width=$w:height=$h:device=$device tv://

