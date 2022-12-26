#!/bin/bash

# https://superuser.com/questions/555401/linux-command-line-tool-to-batch-rename-mp3-files-based-on-id3-tag-info-or-give

kid3-cli -c 'fromtag "%{title}" 1' *.mp3
