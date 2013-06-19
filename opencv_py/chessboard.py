#!/usr/bin/env python

"""
Finds a 9x6 ("inner size") chessboard in the captured frames.
Draw the found corners.
"""

import cv
import pygame
import sys

from pygame.locals import *

# Settings:

PAT_SIZE = (9, 6)

findFlags = (
    cv.CV_CALIB_CB_ADAPTIVE_THRESH
    | cv.CV_CALIB_CB_NORMALIZE_IMAGE
    | cv.CV_CALIB_CB_FILTER_QUADS
)

infoFont = cv.InitFont(cv.CV_FONT_HERSHEY_DUPLEX, 0.75, 0.75)
infoOrigin = (0, 20)
# is it only me who's missing it?
if hasattr(cv, 'CALIB_CB_FAST_CHECK'):
    findFlags |= cv.CALIB_CB_FAST_CHECK

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
    success, corners = cv.FindChessboardCorners(im, PAT_SIZE, findFlags)
    if success:
        cv.DrawChessboardCorners(im, PAT_SIZE, corners, success)
        cv.PutText(im, "Found: (%.1f, %.1f)" %  corners[0], infoOrigin,
            infoFont, (0, 255, 0))
    else:
		cv.PutText(im, "Not found.", infoOrigin, infoFont, (0, 255, 0))
    return cv2pygame(im)

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
