#!/usr/bin/env python

import argparse
import glob
import os
import random

import cv2

MODEL = "haarcascade_frontalface_default.xml"
HAAR_URL = (
    f"https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/{MODEL}"
)


def __id(x):
    return x


def create_detector():
    cascades = [
        MODEL,
        f"/usr/share/opencv/haarcascades/{MODEL}",
        os.path.join(os.path.dirname(__file__), MODEL),
    ]

    if hasattr(cv2, "data"):
        cascades.insert(0, os.path.join(cv2.data.haarcascades, MODEL))

    if not any(os.path.isfile(p) for p in cascades):
        print("No haarcascade_frontalface_default.xml found.")
        answer = input("Downlod from Internet? [Yn] ")
        if not answer or not answer.lower().startswith("n"):
            import urllib

            try:
                response = urllib.request.urlopen(HAAR_URL)
                if response.getcode() == 200:
                    with open(MODEL, "wb") as file:
                        data = response.read()
                        file.write(data)
                    print(f"Downloaded {MODEL}, {len(data):.,} B")
                else:
                    print("GET request failed. Response Code:", response.getcode())
            except urllib.error.URLError as e:
                print("Error:", e)

    for path in cascades:
        if os.path.isfile(path):
            print("Loading face model:", path)
            faceCascade = cv2.CascadeClassifier(path)
            break
    else:
        print("Try:\nsudo apt install opencv-data\nor:")
        print(f"wget {HAAR_URL}")
        exit()

    return faceCascade


parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="+")
parser.add_argument(
    "--inverse", "-v", action="store_true", help="print or show where no faces found"
)
parser.add_argument("--show", action="store_true")
parser.add_argument("--show-all", "-a", action="store_true")
parser.add_argument("--delay", type=int, default=100, help="only used with --show")
parser.add_argument("--progress", action="store_true")
parser.add_argument("--shuffle", action="store_true")

args = parser.parse_args()
faceCascade = create_detector()

fast = args.delay < 500

files = [result for pattern in args.files for result in glob.glob(pattern)]

if args.shuffle:
    random.shuffle(files)

if args.progress:
    try:
        from tqdm import tqdm

        show = tqdm.write
    except ImportError:
        tqdm = __id
        show = print
else:
    tqdm = __id
    show = print

for result in tqdm(files):
    image = cv2.imread(result, cv2.IMREAD_GRAYSCALE)
    # Detect faces in the image

    faces = faceCascade.detectMultiScale(
        image,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        # flags = cv2.CV_HAAR_SCALE_IMAGE
    )

    if (len(faces) == 0) == args.inverse:
        show(result)

    if args.show:
        if not args.show_all and (len(faces) == 0) != args.inverse:
            continue

        for x, y, w, h in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), 255, 2)

        # name for high delay, generic for fast viewing

        if fast:
            cv2.namedWindow("face detection", cv2.WINDOW_NORMAL)
            cv2.imshow("face detection", image)
        else:
            cv2.namedWindow(result, cv2.WINDOW_NORMAL)
            cv2.imshow(result, image)

        res = cv2.waitKey(args.delay) & 0xFF

        if not fast:
            cv2.destroyAllWindows()

        if res == ord("q"):
            break

        if res == ord(" "):
            while cv2.waitKey() == -1:
                pass

cv2.destroyAllWindows()
