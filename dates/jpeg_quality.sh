#!/bin/bash

# identifies JPEG quality (compression level)
# this may not always work very reliably, see:
# https://stackoverflow.com/questions/2024947/is-it-possible-to-tell-the-quality-level-of-a-jpeg
# https://patrakov.blogspot.com/2008/12/jpeg-quality-is-meaningless-number.html
# https://blogs.gnome.org/raphael/2007/10/23/mapping-jpeg-compression-levels-between-adobe-photoshop-and-gimp-24/

identify -format '%f %Q\n' "$@"
