#!/usr/bin/env bash
set -euo pipefail

# uv tool install piper-tts --with pathvalidate
# or:
# pipx install piper-tts
# pipx inject piper-tts pathvalidate

# make sure it's in current directory ;)
# or:
# uvx --from piper-tts python -m piper.download_voices pl_PL-darkman-medium
# or (in pipx - find env with help of `pipx environment`, activate, then):
# python -m piper.download_voices pl_PL-darkman-medium

MODEL="pl_PL-darkman-medium"
CUT=${CUT:-0}
Q=2

mkdir -p prefixed

for in in *.mp3; do
  [ -e "$in" ] || continue
  base="$(basename "$in" .mp3)"
  intro="__intro.wav"
  out="prefixed/${in%.mp3}.mp3"

  piper --model "$MODEL" --output_file "$intro" -- "$base"
  ffmpeg -hide_banner -y -i "$intro" -ar 44100 "$intro.mp3"
# Time signatures go crazy:
#  if [ "$CUT" == "0" ] ; then
#    echo "**** no CUT ****"
#    cp "$in" temp.mp3
#  else
#    echo "**** CUTTING ****"
#    ffmpeg -y -ss $CUT -i "$in" temp.mp3
#  fi
#  echo "file '$intro.mp3'" > inputs.txt
#  echo "file 'temp.mp3'" >> inputs.txt
#  ffmpeg -f concat -i inputs.txt -c copy "$out"
  ffmpeg -hide_banner -y -i "$intro.mp3" -ss $CUT -i "$in" -filter_complex "[0:a][1:a]concat=n=2:v=0:a=1" -c:a libmp3lame -q:a "$Q" "$out"
  rm -f "$intro" "$intro.mp3" # "inputs.txt" temp.mp3 done
done
