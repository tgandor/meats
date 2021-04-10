#!/bin/bash

out_dir=`date --iso`-images
mkdir -p $out_dir
ffmpeg -i "$@" $out_dir/img%06d.jpg

