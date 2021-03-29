#!/bin/bash

if which sntp; then
	sntp -P no -r pool.ntp.org
	exit
fi

if which ntpd; then
	ntpd -qg
	exit
fi

echo 'No suitable tools found.'
