#!/bin/sh

# not sure if this works or not:

# Use V4L2 (preferred) instead of raspivid
# exposure_dynamic_framerate=1 (raspivid --fps 0) - reduce framerate/increase exposure in low light
# scene_mode=8 (raspivid --exposure night) - allow framerate reduction to increase exposure
v4l2-ctl -v width=1296,height=972,pixelformat=H264 \
        --set-ctrl=exposure_dynamic_framerate=1 \
        --set-ctrl=video_bitrate=5000000 \
        --set-ctrl=scene_mode=8

# exec ?
avconv -f h264 -probesize 32 -r 30 -i /dev/video0 -vcodec copy -an -f rtp_mpegts udp://224.0.1.2:5004
