#!/bin/bash

# from: https://askubuntu.com/a/503438/309037
lspci -vnnn | perl -lne 'print if /^\d+\:.+(\[\S+\:\S+\])/' | grep VGA

# somewhat better: https://unix.stackexchange.com/a/185062/98519
glxinfo | egrep "OpenGL vendor|OpenGL renderer*"

# needs bumblebee
# optirun glxinfo | egrep "OpenGL vendor|OpenGL renderer*"

# also useful in many situations
# https://unix.stackexchange.com/a/413282/98519
nvidia-smi -L
