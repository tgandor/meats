#!/bin/bash

ngpu = `nvidia-smi -L | wc -l`
echo "Using $ngpu process slots."
time parallel --jobs $ngpu --process-slot-var=CUDA_VISIBLE_DEVICES whisper ::: "$@"

