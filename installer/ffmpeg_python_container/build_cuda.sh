#!/bin/bash

cd `dirname $0`/../..
time docker build -f installer/ffmpeg_python_container/Dockerfile.cuda . -t ffmpycu

