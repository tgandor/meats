#!/bin/bash

df -h /var/log/journal
du -h /var/log/journal
# this leaves more than 1d behind (active files remain intact)
sudo journalctl --vacuum-time=1d
df -h /var/log/journal
du -h /var/log/journal

