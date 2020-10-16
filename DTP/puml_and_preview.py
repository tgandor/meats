#!/usr/bin/env python

import datetime
import os
import sys

import cv2

puml_file = sys.argv[1]
png_file = puml_file.replace('.puml', '.png')


def build_and_show():
    print(datetime.datetime.now(), 'building', puml_file)
    os.system(f'plantuml {puml_file}')
    img = cv2.imread(png_file)
    cv2.imshow(puml_file, img)


def wait_and_see():
    puml_original = open(puml_file).read()
    while True:
        key = cv2.waitKey(200)
        if key % 256 in (ord('q'), 27):
            return False
        puml_current = open(puml_file).read()
        if puml_current != puml_original:
            return True


keep_running = True
while keep_running:
    build_and_show()
    keep_running = wait_and_see()

