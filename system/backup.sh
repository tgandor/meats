#!/bin/bash

date | tee -a backup.log
echo "Sync" | tee -a backup.log
time rsync -rvc $1 $2 | tee -a backup.log
date | tee -a backup.log
echo "Check" | tee -a backup.log
time rsync -rvc $1 $2 | tee -a backup.log
date | tee -a backup.log
