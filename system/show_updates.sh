#!/bin/bash

# apt-get --just-print upgrade | egrep -v '^Inst |^Conf '
apt list --upgradable | tail -n+2 | cut -d/ -f1 | nl | less
