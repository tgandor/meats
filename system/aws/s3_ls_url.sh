#!/bin/bash
bucket="$1"

aws s3 ls $bucket |\
  awk '{ if ($1 == "PRE") print $2; else print $4 }' |\
  while read key; do 
    echo "$bucket$key"; 
  done
