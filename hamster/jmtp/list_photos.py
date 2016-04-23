#!/usr/bin/env python

import glob
import json
import os


def dump_photos(photo_dir, mounted_dir, target_json):
    files = list(sorted(glob.glob(os.path.join(photo_dir, '*'))))
    mounted_files = [f.replace(photo_dir, mounted_dir) for f in files]
    with open(target_json, 'w') as f:
        json.dump(mounted_files, f, indent=4)
    print("{} files in {}".format(len(files), photo_dir))

photo_dir = '/mnt/extSdCard/DCIM/Camera'
mounted_dir = 'mnt/Card/DCIM/Camera'
target_json = os.path.join(os.path.dirname(__file__), 'photos_card.json')
dump_photos(photo_dir, mounted_dir, target_json)

photo_dir = '/mnt/sdcard/DCIM/Camera'
mounted_dir = 'mnt/Phone/DCIM/Camera'
target_json = os.path.join(os.path.dirname(__file__), 'photos_phone.json')
dump_photos(photo_dir, mounted_dir, target_json)

