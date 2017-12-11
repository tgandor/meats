#!/bin/bash


# playing with MPlayer ( https://raspberrypi.stackexchange.com/a/27656/55667 )
# mplayer -fps 200 -demuxer h264es ffmpeg://tcp://<YOUR_IP>:2222

# this can be played in VLC with URL:
# (TODO: probably needs very new VLC...)

# fullHD, default BTW, does not use binning / view full frame
# raspivid $* -w 1920 -h 1080 -t 0 -l -o tcp://0.0.0.0:3333
# full frame is 2592 x 1944, and 1/4 will use 2x2 binning:

raspivid $* -fps 7.5 -w 1296 -h 972 -t 0 -l -o tcp://0.0.0.0:3333
