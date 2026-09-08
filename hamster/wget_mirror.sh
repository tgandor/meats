#!/bin/bash

# Originally from here:
# https://www.guyrutenberg.com/2014/05/02/make-offline-mirror-of-a-site-using-wget/

# maybe some further tweaking will follow
wget --mirror --convert-links --adjust-extension --page-requisites \
    --no-parent --wait=2 --random-wait --restrict-file-names=windows "$@"
