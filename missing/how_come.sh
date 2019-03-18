#!/bin/bash

if [ "$1" == "" ]; then
    echo "Usage: $0 <command>"
    echo "Prints package and apt-get command for installing it."
    exit
fi

function processCommand {
    if ! which $1 > /dev/null; then
        echo >&2 "Command not found: $1"
        return
    fi

    cmd_path=`which $1`

# sometimes a command is symlinked via alternatives:

    real_path=`readlink -f $cmd_path`

    if [ "$real_path" != "$cmd_path" ] ; then
        # special case: snaps
        if [ "$real_path" == "/usr/bin/snap" ] ; then
            echo >&2 "This comes from a snap package"
            echo >&2 "Probably just:"
            echo >&2 "sudo snap install $1"
            return
        fi

        echo >&2 "$real_path"
        cmd_path=$real_path
    fi

    dpkg -S $cmd_path | awk '{ gsub(/:$/, "", $1); print "sudo apt install " $1;}' >&2
    echo >&2 "---"
}

echo "#!/bin/bash"

# single command: simple snippet

if [ "$2" == "" ] ; then
    processCommand $1
    dpkg -S $cmd_path | awk '{ gsub(/:$/, "", $1); print "if ! which '$1' >/dev/null; then\n    sudo apt install " $1 "\nfi"; }'
    exit
fi

echo 'missing=""'

while [ "$1" != "" ] ; do
    processCommand $1
    dpkg -S $cmd_path | awk '{ gsub(/:$/, "", $1); print "if ! which '$1' >/dev/null; then\n\tmissing=\"$missing " $1 "\"\nfi"; }'
    shift
done

echo 'if [ -n "$missing" ] ; then'
echo '    echo "Missing packages: $missing"'
echo '    sudo apt install $missing'
echo 'fi'
