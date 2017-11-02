#!/bin/bash

if [ -z "$2" ] ; then
	echo "Usage: $0 source target"
	exit
fi

mkdir -p $2

target=`readlink -f $2`
info_dir=`dirname $target`/_info_`basename $2`
mkdir -p $info_dir

time (
date
echo "Listing $2"
rm $info_dir/target_pre_backup.txt
pushd $2
time `dirname $0`/generate_filelist.sh $info_dir/target_pre_backup.txt
popd

date
echo "Listing $2"
rm $info_dir/source_pre_backup.txt
pushd $1
time `dirname $0`/generate_filelist.sh $info_dir/source_pre_backup.txt
popd

date
echo "rsyncing..."
time rsync -r $1 $2
echo "done"

pushd $info_dir
date
echo "sorting filelists"
time sort target_pre_backup.txt > sorted_target_pre_backup.txt
time sort source_pre_backup.txt > sorted_source_pre_backup.txt
date

echo "diffing filelists"
time comm -23 sorted_target_pre_backup.txt sorted_source_pre_backup.txt > removal_candidates.txt
time comm -13 sorted_target_pre_backup.txt sorted_source_pre_backup.txt > newly_backedup.txt
date
) | tee $info_dir/backup.log
