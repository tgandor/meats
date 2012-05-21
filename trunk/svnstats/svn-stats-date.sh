#!/bin/bash

date_requested=$1
if [ -z $date_requested ] ; then 
	date_requested=today
fi

date_formatted=`date --iso -d $date_requested`

if [ -z $date_formatted ] ; then
	echo "Wrong date: $date_requested"
	echo "Usage: $0 DATE_DESCRIPTION"
	echo "where DATE_DESCRIPTION is an expression acceptable by date -d"
	echo "Default: current day"
	exit
fi

svn log -r "{$date_formatted}:HEAD" $LOGURL | awk '/^r[1-9]/ { print $3; }' | sort | uniq -c | sort -n
