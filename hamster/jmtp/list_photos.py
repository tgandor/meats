#!/usr/bin/env python

import glob
import json
import os

photo_dir = '/mnt/extSdCard/DCIM/Camera'
mounted_dir = 'mnt/Card/DCIM/Camera'

files = list(sorted(glob.glob(os.path.join(photo_dir, '*'))))
mounted_files = [f.replace(photo_dir, mounted_dir) for f in files]

target_json = os.path.join(os.path.dirname(__file__), 'photos.json')

with open(target_json, 'w') as f:
    json.dump(mounted_files, f, indent=4)
