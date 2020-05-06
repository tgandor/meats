#!/bin/bash

# Credits:
# https://stackoverflow.com/a/12246397/1338797

# There are some alternatives:
# {apt install, pacman -S} catdoc
# pip install xlsx2csv (for CSV actually)

convert() {
    echo "$1"
    # not so good for nested stuff, so:
    working_dir=`dirname "$1"`
    name=`basename "$1"`
    pushd "$working_dir"
    libreoffice --headless --convert-to "txt:Text (encoded):UTF8" "$name"
    popd
}

find_and_convert() {
    echo "Searching for $1 ..."
    find -name "$1" | while read f; do
        convert "$f"
    done
}

find_and_convert '*.docx'
find_and_convert '*.doc'
find_and_convert '*.xlsx'
find_and_convert '*.xls'
