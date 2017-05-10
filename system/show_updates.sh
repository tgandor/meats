#!/bin/bash

#apt-get -u upgrade
apt-get --just-print upgrade | egrep -v '^Inst |^Conf '
