#!/usr/bin/env python

from __future__ import  print_function

import argparse
import base64
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument('har_files', nargs='+')
args = parser.parse_args()

def unpack_single(har_filename):
    total_output = 0

    with open(har_filename) as har_file:
        har = json.load(har_file)

    for i, entry in enumerate(har['log']['entries']):
        filename = os.path.basename(entry['request']['url'])
        if not filename:
            print('Bad filename in entry', i)
            continue

        mime_type = entry['response']['content']['mimeType']
        print('Entry', i, mime_type, filename, 'status', entry['response']['status'])
        data = entry['response']['content'].get('text')

        if not data:
            print('No text in response')
            continue

        if entry['response']['content'].get('encoding') == 'base64':
            data = base64.b64decode(data)

        if os.path.exists(filename):
            print(filename, 'EXISTS! Not overwriting.')
            continue

        with open(filename, 'wb') as data_file:
            data_file.write(data)
        total_output += len(data)
        print('File {} - {:,} bytes written.'.format(filename, len(data)))
    print('Done extracting:', har_filename, 'total: {:,} B.'.format(total_output))
    return total_output

if __name__ == '__main__':
    total = 0
    for har in args.har_files:
        total += unpack_single(har)
    print('Finished. Extracted {:,} B'.format(total))
