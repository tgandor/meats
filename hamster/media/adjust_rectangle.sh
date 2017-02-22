#!/bin/bash

# Source: https://incenp.org/notes/2012/video-cropping.html
# needs ~/.mplayer/crop input config

mplayer -vf rectangle -input conf=crop "$1"
