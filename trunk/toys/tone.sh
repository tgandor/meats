#!/bin/bash
gcc -o tone.exe tone.c -lm
./tone.exe
sox -r 44100 -e signed -b 16 tone.raw tone.wav
play tone.wav

