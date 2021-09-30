#!/bin/bash

# .%(ext)s required because of -x, error otherwise.
# would like to --embed-thumbnail, but it only works for mp3 and m4a (not opus)
youtube-dl -x --write-thumbnail -o "%(playlist_index)02d-%(title)s.%(ext)s" "$@"
