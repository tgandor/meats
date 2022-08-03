#!/bin/bash

# threshold bright color to white, make monochrome
mogrify -channel RGB -white-threshold 45% -colorspace gray "$@"
