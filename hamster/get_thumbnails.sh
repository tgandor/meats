#!/bin/bash

if [ "$1" == "-n" ] ; then
    # default name (title)-(id)
    xargs -n1 yt-dlp --skip-download --write-thumbnail
else
    # usually gets WebP, but there is another way of getting JPGs
    xargs -n1 yt-dlp --skip-download --write-thumbnail --output "%(id)s"
fi
