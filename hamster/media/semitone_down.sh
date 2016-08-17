#!/bin/bash

# https://trac.ffmpeg.org/wiki/How%20to%20speed%20up%20/%20slow%20down%20a%20video
# semitone = frequency * 2 ^ (-1/12) = frequency * 0.9438743126816935
# semitone = period * 2 ^ (1/12) = period * 1.0594630943592953

if [ -z "$1" ]; then
	echo "Usage: $0 <file_to_change_pitch>"
	exit
fi

mkdir -p original
mv "$1" original

# does this NOT transpose (keep pitch?)
# ffmpeg -i "original/$1" -filter_complex "[0:v]setpts=1.0594630943592953*PTS[v];[0:a]atempo=0.9438743126816935[a]" -map "[v]" -map "[a]" "$1"

# nvm, 14.04 has avconv, with no atempo

ffmpeg -i "original/$1" -filter_complex "[0:v]setpts=1.0594630943592953*PTS[v];[0:a]asetpts=1.0594630943592953[a]" -map "[v]" -map "[a]" "$1"

