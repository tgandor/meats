#!/bin/bash

if ! which cvlc ; then
	sudo apt-get install vlc-nox
fi

# Had problems on B+ ... ?
# https://raspberrypi.stackexchange.com/a/26075/55667

sudo modprobe bcm2835-v4l2

cvlc v4l2:///dev/video0 --v4l2-width 1920 --v4l2-height 1080 --v4l2-chroma h264 --sout '#standard{access=http,mux=ts,dst=0.0.0.0:12345}'
