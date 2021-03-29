#!/bin/bash
scp -o "UserKnownHostsFile /dev/null" "$@"
