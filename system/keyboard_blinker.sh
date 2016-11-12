#!/bin/bash

# http://www.commandlinefu.com/commands/view/3869/turn-onoff-keyboard-leds-via-commandline
# toggle scroll lock keyboard led
while true; do xset led 3; sleep 0.5; xset -led 3; sleep 0.5; done
