#!/usr/bin/env python

import json
import yaml
import sys


def convert(filename):
    with open(filename, 'r') as fp:
        config = yaml.load(fp, loader=yaml.SafeLoader)
    new_config = {
        key: json.dumps(json.loads(val), indent=2)
        for key, val in config.items()
    }
    with open(filename, 'w') as fp:
        yaml.dump(new_config, fp)


for fn in sys.argv[1:]:
    convert(fn)
