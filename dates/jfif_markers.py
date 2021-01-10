#!/usr/bin/env python
from __future__ import print_function
import argparse

# info source: https://www.impulseadventure.com/photo/jpeg-decoder.html

parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+')
parser.add_argument('--verbose', '-v', action='store_true')
parser.add_argument('--skip-scan', '-s', action='store_true')
parser.add_argument('--select', '-m', help='markers to show')
parser.add_argument('--name', '-n', action='store_true',
                    help='prefix with filename')
args = parser.parse_args()


def decode_sof0(data):
    # http://www.vip.sugovica.hu/Sardi/kepnezo/JPEG%20File%20Layout%20and%20Format.htm
    return {
        "bits": data[0],
        "height": data[1] * 256 + data[2],
        "width": data[3] * 256 + data[4],
        "num_components": data[5],
        "components": [
            {
                "id": data[6+3*i],
                "v_sampling": data[7+3*i] & 0xf,
                "h_sampling": data[7+3*i] >> 4,
                "QT": data[8+3*i],
            }
            for i in range(data[5])
        ]
    }


decodable = {
    "SOF0": decode_sof0
}

names = {
    0xc4: 'DHT',
    0xd8: 'SOI',
    0xd9: 'EOI',
    0xda: 'SOS',
    0xdb: 'DQT',
    0xfe: 'COM',
}
markers = {}  # reverse names
for d, m in names.items():
    markers[m] = d

# APP_x
for i, d in enumerate(range(0xe0, 0xef+1)):
    m = 'APP{}'.format(i)
    names[d] = m
    markers[m] = d

standalone = {
    0,  # not a marker
    0x01,  # TEM
    0xd8,  # SOI
    0xd9,  # EOI
    # *range(0xd0, 0xd7+1), # RST
}

# SOF_x - Start of Frame x
not_sof = {
    0xc4,  # DHT Define Huffman Table
    0xc8,  # JPG JPEG Extensions
    0xcc,  # DAC Define Arithmetic Coding
}
for i, d in enumerate(range(0xc0, 0xcf+1)):
    if d in not_sof:
        continue
    m = 'SOF{}'.format(i)
    names[d] = m
    markers[m] = d

# RST_x - Restart Marker x
for i, d in enumerate(range(0xd0, 0xd7+1)):
    standalone.add(d)
    m = 'RST{}'.format(i)
    names[d] = m
    markers[m] = d

to_show = None
if args.select:
    if args.select not in markers:
        print('Unsupported JFIF marker:', args.select)
        exit()
    to_show = markers[args.select]

for filename in args.files:
    with open(filename, 'rb') as f:
        while True:
            ch = f.read(1)
            if not ch:
                break
            c = ord(ch)
            if c == 0xff:
                d = ord(f.read(1))

                if d in standalone:
                    if d == to_show:
                        print(
                            filename if args.name else '',
                            "%6d" % f.tell(),
                            hex(256*c+d)[2:],
                            '%5s' % names.get(d, ' ? '),
                            '(standalone)',
                        )
                    continue

                h = ord(f.read(1))
                l = ord(f.read(1))
                size = 256 * h + l
                data = f.read(size - 2)  # 2 bytes already there
                if (to_show is None or d == to_show) and d:
                    print(
                        filename if args.name else '',
                        "%6d" % f.tell(),
                        hex(256*c+d)[2:],
                        '%5s' % names.get(d, ' ? '),
                        'size: {:,}'.format(size),
                        repr(data) if args.verbose else ''
                    )

                if args.select and args.select in decodable and d == to_show:
                    print(decodable[args.select](data))

                if d == markers['SOS'] and args.skip_scan:
                    break
