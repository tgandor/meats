#!/bin/bash

# another problem with KDE in this directory...
# https://unix.stackexchange.com/questions/72869/how-to-restart-kde-window-decorations-without-loosing-the-running-x-session

DISPLAY=:0 kwin --replace &
