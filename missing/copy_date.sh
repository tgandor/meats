#!/bin/bash

if [ "$1" == "-f" ] ; then
    # filename-appropriate
    date +%F_%a_%H.%M | xargs ~/meats/missing/clipboard_copy.py
    date +%F_%a_%H.%M
elif [ "$1" == "-r" ] ; then
    # 'raw' date (no time)
    date +%F | xargs ~/meats/missing/clipboard_copy.py
    date +%F
else
    date +%F_%a_%R | xargs ~/meats/missing/clipboard_copy.py
    date +%F_%a_%R
fi

