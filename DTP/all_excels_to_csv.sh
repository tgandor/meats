#!/bin/bash

if ! which xlsx2csv >/dev/null; then
    sudo apt install xlsx2csv
fi

find -name *.xlsx | while read f ; do
    csv="$(dirname "$f")/$(basename "$f" .xlsx).csv"
    echo xlsx2csv "$f" "$csv"
    xlsx2csv "$f" "$csv"
done

if ! which xls2csv >/dev/null; then
    sudo apt install catdoc
fi

find -name *.xls | while read f ; do
    csv="$(dirname "$f")/$(basename "$f" .xls).csv"
    echo xls2csv "$f" '>' "$csv"
    xls2csv "$f" > "$csv"
done
