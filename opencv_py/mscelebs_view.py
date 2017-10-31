'''
https://www.microsoft.com/en-us/research/project/ms-celeb-1m-challenge-recognizing-one-million-celebrities-real-world/

File format: text files, each line is an image record containing 6 columns, delimited by TAB.
Column1: Freebase MID
Column2: Query/Name
Column3: ImageSearchRank
Column4: ImageURL
Column5: PageURL
Column6: ImageData_Base64Encoded
'''

import cv2
import gzip
import argparse
import base64
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('file')
args = parser.parse_args()


def open_file(name):
    if name.endswith('.tsv.gz'):
        return gzip.open(name, 'r')
    elif name.endswith('.tsv'):
        return open(name, 'r')
    raise ValueError('Wrong file type.')


i = 0
with open_file(args.file) as f:
    while True:
        line = f.readline()
        i += 1
        if not line:
            break

        try:
            code, number, image_url, page_url, face_id, short_data, image_data = line.split()
        except ValueError:
            print(i, 'Error processing line:', line.split()[:-1], '...')
            print('=' * 70)
            continue

        # print(code, number, image_url, page_url, face_id, short_data, repr(base64.b64decode(short_data)))
        # exit()

        raw_data = np.fromstring(base64.b64decode(image_data), np.uint8)
        image = cv2.imdecode(raw_data, cv2.IMREAD_COLOR)
        print(i, code, number, image_url, page_url, face_id, short_data, image.shape)
        cv2.imshow('Celebrity', image)
        key = cv2.waitKey(0) & 0xff
        if key in (27, ord('q')):
            break
