#!/bin/bash

if [ -z "$1" ] ; then
    echo "Usage: $0 user@host [-p port etc.]"
    echo "Adds your public SSH key (id_rsa.pub, id_ed25519.pub, etc.) to user's .ssh/authorized_keys"
    exit
fi

# List of supported key types (add more if needed)
KEYTYPES=(id_ed25519 id_rsa)
KEYFOUND=""

for keytype in "${KEYTYPES[@]}"; do
    if [ -f "$HOME/.ssh/${keytype}" ]; then
        KEYFOUND="$keytype"
        break
    fi
done

if [ -z "$KEYFOUND" ]; then
    # No key found, generate ed25519 by default
    echo "No SSH key found. Generating id_ed25519 (recommended)..."
    ssh-keygen -t ed25519 -f "$HOME/.ssh/id_ed25519"
    KEYFOUND="id_ed25519"
fi

PUBKEY="$HOME/.ssh/${KEYFOUND}.pub"

if ( ssh -o PasswordAuthentication=no "$@" pwd ) ; then
    echo "You are already authorized!"
    exit
fi

cat "$PUBKEY" | ssh "$@" "mkdir -p .ssh ; tee -a .ssh/authorized_keys"

if ( ssh -o PasswordAuthentication=no "$@" pwd ) ; then
    echo "Success!"
else
    echo "Something doesn't work. Change to 0600?"
fi
