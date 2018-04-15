#!/bin/bash

apt-get --just-print upgrade | egrep -v '^Inst |^Conf '
apt list --upgradeable 
