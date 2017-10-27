#!/bin/bash
raspivid $* -w 1920 -h 1080 -t 0 -l -o tcp://0.0.0.0:3333
