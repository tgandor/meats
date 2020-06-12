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
    pushd "$working_dir" >/dev/null
    libreoffice --headless --convert-to "$2" $3 "$name"
    popd >/dev/null
}

find_and_convert() {
    echo "... Searching for $1 ..."
    find -name "$1" | while read f; do
        convert "$f" "$2" $3
    done
}

find_and_convert '*.docx' 'txt:Text (encoded):UTF8'
find_and_convert '*.doc' 'txt:Text (encoded):UTF8'
# this is so ghasty:
# https://unix.stackexchange.com/questions/259361/specify-encoding-with-libreoffice-convert-to-csv
find_and_convert '*.xlsx' csv --infilter=CSV:44,34,76,1
find_and_convert '*.xls' csv --infilter=CSV:44,34,76,1
