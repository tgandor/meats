#!/bin/bash

if ! which cvlc ; then
	sudo apt-get install vlc-nox
fi

# Had problems on B+ ... ?
# https://raspberrypi.stackexchange.com/a/26075/55667
# sudo modprobe bcm2835-v4l2
# cvlc v4l2:///dev/video0 --v4l2-width 1920 --v4l2-height 1080 --v4l2-chroma h264 --sout '#standard{access=http,mux=ts,dst=0.0.0.0:12345}'

# This:
# raspivid -o - -t 0 -n -w 1296 -h 927 -fps 15 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://0.0.0.0:8554/}' :demux=h264
# results in:
# core debug: no access_demux modules matched
# core debug: creating access 'rtsp' location='192.168.1.1:8554', path='(null)'
# core debug: looking for access module matching "rtsp": 25 candidates
# core debug: net: connecting to 192.168.1.1 port 8554
# core debug: connection succeeded (socket = 32)
# access_realrtsp debug: rtsp connected
# access_realrtsp warning: only real/helix rtsp servers supported for now
# core debug: no access modules matched
# core error: open of `rtsp://192.168.1.1:8554' failed
# core debug: dead input

# This finally works +- OK:
# ( watch with MRL: http://<YOUR_IP>:8080/ )
raspivid -o - -t 0 -n -w 1296 -h 972 -fps 15 $* | cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=0.0.0.0:8080}' :demux=h264

# mplayer also plays it, but there are MV errors in I frames... 
# (and visual artifacts in the bottom 1/4 of the frame)

# But, with FPS specified, it played fine:
# mplayer -fps 15 http://<YOUR_IP>:8080/
