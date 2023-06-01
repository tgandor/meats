#!/bin/bash

time parallel ffmpeg -i {} {.}.opus ::: "$@"
