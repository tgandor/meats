#!/bin/bash

# Thanks to: https://www.endpoint.com/blog/2010/04/09/tip-find-all-non-utf8-files

if which isutf8 > /dev/null ; then
# good alternative
    find . -type f -exec isutf8 {} +
else 
    find . -type f | xargs -I {} bash -c "iconv -f utf-8 -t utf-16 {} &>/dev/null || echo {}"
fi

