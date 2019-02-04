#!/bin/bash

destination_spec=""

if lpstat -p -d | grep -q 'no system default'
then
    destination=`lpstat -p | awk 'NR==1 { print $2 }'`
    echo "Warning: guessing destination: $destination"
    destination_spec="-d $destination"
fi

lp -o media=a4 -o sides=two-sided-long-edge $destination_spec "$@"
