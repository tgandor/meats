#!/usr/bin/env python

import base64
import glob
import serial
import time

port = glob.glob('/dev/ttyUSB*')[0]
baudrate = 460800
parity = serial.PARITY_NONE
rtscts = False
xonxoff = False

save_b64 = False
save_raw = False
save_png = True
save_txt = True

img_xsize = 320
img_ysize = 240

# gbr565 decoding - for PNG

r_shft = 11
r_bits = 5
r_mask = (1 << r_bits) - 1

g_shft = 5
g_bits = 6
g_mask = (1 << g_bits) - 1

b_shft = 0
b_bits = 5
b_mask = (1 << b_bits) - 1

def main():
    print("Using port: {}".format(port))
    ttyUSB = serial.serial_for_url(port, baudrate, parity=parity, rtscts=rtscts, xonxoff=xonxoff, timeout=1)

    while True:
        line = ttyUSB.readline()
        if line == b'':
            continue
        if line.startswith(b'SNAPSHOT'):
            process_snapshot(ttyUSB, line)
        else:
            print('Info: {}'.format(repr(line)))


def save_png(filename, data):
    try:
        from PIL import Image
    except ImportError:
        print("Missing PIL/Pillow library. Please turn off 'save_png' configuration")
        exit()
    try:
        import numpy as np
    except ImportError:
        print("Missing numpy library. Please turn off 'save_png' configuration")
        exit()

    original = np.fromstring(data, dtype=np.uint16).reshape((img_ysize, img_xsize))

    rgb_array = np.zeros((img_ysize, img_xsize, 3), dtype=np.uint8)

    for i in range(img_ysize):
        for j in range(img_xsize):
            rgb_array[i][j][0] = ((original[i][j] >> r_shft) & r_mask) << (8 - r_bits)
            rgb_array[i][j][1] = ((original[i][j] >> g_shft) & g_mask) << (8 - g_bits)
            rgb_array[i][j][2] = ((original[i][j] >> b_shft) & b_mask) << (8 - b_bits)

    img = Image.fromarray(rgb_array)
    img.save(filename)


def process_snapshot(serial_, header):
    lines_to_read = int(header.split()[1])
    print('Reading snapshot of {} lines...'.format(lines_to_read))
    lines = []
    for _ in range(lines_to_read):
        line = serial_.readline()
        lines.append(line.decode().strip())
    line = serial_.readline()
    # print(line)
    assert line.startswith(b'END_SNAPSHOT')
    timestamp = time.strftime("%y%m%d_%H%M%S")
    data = '\n'.join(lines)

    if save_b64:
        snapshot_filename = timestamp + '.b64'
        with open(snapshot_filename, 'w') as f:
            f.write(data)
        print('Snapshot base64 saved to file: {}'.format(snapshot_filename))
    decoded_raw = base64.b64decode(data)

    if save_raw:
        snapshot_filename = timestamp + '.raw'
        with open(snapshot_filename, 'wb') as f:
            f.write(decoded_raw)
        print('Snapshot raw data saved to file: {}'.format(snapshot_filename))

    if save_png:
        snapshot_filename = timestamp + '.png'
        save_png(snapshot_filename, decoded_raw)

    if save_txt:
        print('Waiting for Zbar results...')

        while True:
            line = serial_.readline()
            if line.startswith(b'Scan result: '):
                result = int(line.split()[2])
                break

        if result <= 0:
            with open(timestamp + '_FAIL.txt', 'wb') as f:
                f.write(line)
            print('No barcode, Zbar returned {}'.format(result))
            return

        header = line

        while True:
            line = serial_.readline()
            if line.startswith(b'Decoded barcode: '):
                # barcode = line.split(maxsplit=2)[2].decode().strip() # Py3 ...
                barcode = line.split(None, 2)[2].decode().strip()
                break

        print('Saving results, Zbar {}, Barcode: {}'.format(result, barcode))
        
        with open(timestamp + '_OKAY.txt', 'wb') as f:
            f.write(header)
            f.write(line)


if __name__ == '__main__':
    main()
