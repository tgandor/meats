#!/usr/bin/env python

"""
Found on the Internet: a demo of grabbing webcam images with
OpenCV -> converting them to PIL Images -> displaying them with pygame.
"""

import pygame
import Image
from pygame.locals import *
import sys

import opencv
from opencv import highgui

camera = highgui.cvCreateCameraCapture(0)

def get_image():
    im = highgui.cvQueryFrame(camera)
    return opencv.adaptors.Ipl2PIL(im)

fps = 40.0
pygame.init()
window = pygame.display.set_mode((640,480))
pygame.display.set_caption("WebCam Demo - opencv module")
screen = pygame.display.get_surface()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT or event.type == KEYDOWN:
            print event
            pygame.quit()
            sys.exit(0)
    im = get_image()
    pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
    screen.blit(pg_img, (0,0))
    pygame.display.flip()
    pygame.time.delay(int(1000 * 1.0/fps))
