#!/bin/bash

# to consider: --write-info-json
youtube-dl --extract-audio --audio-format mp3 --embed-thumbnail --output "%(playlist_index)02d-%(title)s.%(ext)s" "$@"
