#!/usr/bin/env python

# generated code ;)

import os
from PIL import Image

# Define the minimum width and height
min_width, min_height = 1000, 1000

# Get a list of all files in the current directory
files = os.listdir()

# Loop through all files and check if they are images
for file in files:
    if (
        file.endswith(".jpg")
        or file.endswith(".jpeg")
        or file.endswith(".png")
        or file.endswith(".webp")
    ):
        # Open the image and get its dimensions
        with Image.open(file) as img:
            width, height = img.size
        # If the image is smaller than the minimum size, delete it
        if width < min_width or height < min_height:
            os.remove(file)
            print(f"Deleted {file} ({width}x{height})")
