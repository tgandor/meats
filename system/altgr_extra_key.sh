#!/bin/bash

# check xev for the keycode. Works in X11, may not elswhere.
xmodmap -e "keycode 94 = ISO_Level5_Shift"
