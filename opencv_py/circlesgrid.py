#!/usr/bin/env python

"""
Find a symmetric (straight) 5x4 circles grid.
Draw the found circle centers.
"""

import cv2
import pygame
import sys

from pygame.locals import *

# Settings:

PAT_SIZE = (5, 4)

findFlags = (
    cv2.CALIB_CB_SYMMETRIC_GRID
    #| cv2.CALIB_CB_CLUSTERING
)

infoOrigin = (0, 20)

camera = cv2.VideoCapture(0)

def cv22pygame(im):
    # I'm blue, da ba dee... - for that skip next line
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    return pygame.image.frombuffer(im.tostring(), (im.shape[1], im.shape[0]), "RGB")

def get_image():
    succes, im = camera.read()
    im = cv2.flip(im, 1) # mirror effect
    success, corners =  cv2.findCirclesGridDefault(im, PAT_SIZE, flags=findFlags)
    if success:
        # import pdb; pdb.set_trace()
        cv2.drawChessboardCorners(im, PAT_SIZE, corners, success)
        cv2.putText(im, "Found: (%.1f, %.1f)" %  tuple(corners[0, 0].tolist()), 
                infoOrigin, cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 255, 0))
    else:
		cv2.putText(im, "Not found.", infoOrigin, cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 255, 0))
    return cv22pygame(im)

fps = 30.0
pygame.init()
window = pygame.display.set_mode((640,480))
pygame.display.set_caption("WebCam: Chessboard")
screen = pygame.display.get_surface()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT or event.type == KEYDOWN:
            print event
            pygame.quit()
            sys.exit(0)
    pg_img = get_image()
    screen.blit(pg_img, (0,0))
    pygame.display.flip()
    # pygame.time.delay(int(1000 * 1.0/fps))
