#!/bin/bash

if [[ -z $1 ]]; then
    echo "Usage: $0 [ssh_options] <[user@]server_ip_or_hostname> [upload|download]"
    echo "Download is default if not specified."
    exit 1
fi

if ! command -v pv &> /dev/null; then
    echo "Error: 'pv' command not found. Please install it to use this script."
    exit 1
fi

echo "Press Ctrl+C to stop the test."
# echo "${!#} - last arg, same as: ${@: -1}"
# echo "${@:1:$#-1} - rest args, no last."

if [[ "${!#}" == "upload" ]]; then
    pv -s 100M -S -arptbe /dev/zero | ssh "${@:1:$#-1}" "cat > /dev/null"
elif [[ "${!#}" == "download" ]]; then
    pv -s 100M -S -arptbe /dev/zero | ssh "$@" "cat > /dev/null"
    ssh "${@:1:$#-1}" "cat /dev/zero" | pv -s 100M -S -arptbe | cat > /dev/null
else
    # Download test, no args
    ssh "$@" "cat /dev/zero" | pv -s 100M -S -arptbe | cat > /dev/null
fi
