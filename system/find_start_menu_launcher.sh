#!/bin/bash

if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <search_term> [search_term ...]"
    echo "Example: $0 weasis"
    echo "Example: $0 thunderbird"
    exit 1
fi

grep -Ril "$@" ~/.local/share/applications /usr/share/applications
