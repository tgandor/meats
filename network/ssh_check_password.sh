#!/bin/bash
# https://unix.stackexchange.com/questions/15138/how-to-force-ssh-client-to-use-only-password-auth
ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no "$@"
