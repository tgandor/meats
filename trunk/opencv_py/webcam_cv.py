#!/usr/bin/env python

"""
Translated from webcam_ocv.py to use the newer (but not newest?) cv module:
Grabbing frames with OpenCV and displaying them with pygame.
Should need no PIL.
"""

import cv
import pygame
import sys

from pygame.locals import *

camera = cv.CreateCameraCapture(0)

def cv2pygame(im):
    # I'm blue, da ba dee... - for that it's enough to:
    # return pygame.image.frombuffer(im.tostring(), cv.GetSize(im), "RGB")
    im_rgb = cv.CreateMat(im.height, im.width, cv.CV_8UC3)
    cv.CvtColor(im, im_rgb, cv.CV_BGR2RGB)
    return pygame.image.frombuffer(im_rgb.tostring(), cv.GetSize(im_rgb), "RGB")

def get_image():
    im = cv.QueryFrame(camera)
    cv.Flip(im, flipMode=1) # mirror effect
    return cv2pygame(im)

fps = 40.0
pygame.init()
window = pygame.display.set_mode((640, 480))
pygame.display.set_caption("WebCam Demo - cv module")
screen = pygame.display.get_surface()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT or event.type == KEYDOWN:
            print event
            pygame.quit()
            sys.exit(0)
    pg_img = get_image()
    screen.blit(pg_img, (0, 0))
    pygame.display.flip()
    pygame.time.delay(int(1000 * 1.0/fps))
