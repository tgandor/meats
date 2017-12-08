#!/bin/bash

# fullHD, default BTW, does not use binning / view full frame
# raspivid $* -w 1920 -h 1080 -t 0 -l -o tcp://0.0.0.0:3333
# full frame is 2592 x 1944, and 1/4 will use 2x2 binning:

raspivid $* -fps 7.5 -w 1296 -h 972 -t 0 -l -o tcp://0.0.0.0:3333
