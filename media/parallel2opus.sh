#!/bin/bash

time parallel ffmpeg -hide_banner -i {} $OPTS {.}.opus ::: "$@"
