#!/usr/bin/env python

import argparse
import glob
import os

HEADER = """\
<!doctype html>
<html lang="en">
  <head>
    <title>TITLE - Image Index</title>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="<?php echo $bs ?>"
        integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4"
        crossorigin="anonymous">

    <style>
    .container {
        width: auto;
        max-width: 1280px;
        padding: 0 15px;
    }
    </style>
  </head>

  <body>
    <div class="container">
        <div class="jumbotron d-none d-md-block">
            <h1>TITLE</h1>
            <p class="lead">Pictures in folder.</p>
        </div>
"""

FOOTER = """\
    </div>
  </body>
</html>
"""

ENTRY = """\
            <div class="col-sm-6 col-md-4 col-lg-3 py-3">
                <p>{number}. <a href="{path}">{path}</a></p>
                <a href="{path}">
                    <img src="{path}" style="width: 100%;">
                </a>
            </div>
"""

IMGS = ".jpg .jpeg .avif .webp .png .gif .bmp".split()


def is_img(filename):
    name = filename.lower()
    for format in IMGS:
        if name.endswith(format):
            return True
    return False


parser = argparse.ArgumentParser()
parser.add_argument("--recursive", "-r", action="store_true", help="glob recursively")
args = parser.parse_args()

candidates = (
    glob.glob("**/*.*", recursive=True) if args.recursive else glob.glob("*.*")
)
print(len(candidates), "files found")
parent = os.path.basename(os.getcwd())

files = sorted(filter(is_img, candidates))

with open("index.html", "w") as idx:
    idx.write(HEADER.replace("TITLE", parent))
    for number, path in enumerate(files, start=1):
        idx.write(ENTRY.format(**locals()))
    idx.write(FOOTER)
