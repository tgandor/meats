#!/bin/bash

out_dir=`date --iso`-images
mkdir -p $out_dir
ffmpeg -hide_banner -i "$@" -vf mpdecimate $out_dir/img%06d.jpg
