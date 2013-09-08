#!/usr/bin/env python

"""
Finds a 9x6 ("inner size") chessboard in the captured frames.
Draw the found corners.
"""

import cv
import cv2 # only flag value
import numpy
import pygame
import sys
import time

from pygame.locals import *


# Settings:

PAT_SIZE = (9, 6)
IMG_SIZE = (640, 480)
findFlags = (
    cv.CV_CALIB_CB_ADAPTIVE_THRESH
    | cv.CV_CALIB_CB_NORMALIZE_IMAGE
    | cv.CV_CALIB_CB_FILTER_QUADS
    | cv2.CALIB_CB_FAST_CHECK
)

infoFont = cv.InitFont(cv.CV_FONT_HERSHEY_DUPLEX, 0.75, 0.75)
infoOrigin = (0, 20)

camera = cv.CreateCameraCapture(0)

def cv2pygame(im):
    # I'm blue, da ba dee... - for that it's enough to:
    # return pygame.image.frombuffer(im.tostring(), cv.GetSize(im), "RGB")
    im_rgb = cv.CreateMat(im.height, im.width, cv.CV_8UC3)
    cv.CvtColor(im, im_rgb, cv.CV_BGR2RGB)
    return pygame.image.frombuffer(im_rgb.tostring(), cv.GetSize(im_rgb), "RGB")

def get_image():
    im = cv.QueryFrame(camera)
    # cv.Flip(im, flipMode=1) # mirror effect
    success, corners = cv.FindChessboardCorners(im, PAT_SIZE, findFlags)
    if success:
        cv.DrawChessboardCorners(im, PAT_SIZE, corners, success)
        cv.PutText(im, "Found: (%.1f, %.1f)" %  corners[0], infoOrigin,
            infoFont, (0, 255, 0))
        cam_matrix = cv.CreateMat(3, 3, cv.CV_32F)
        dist_coeff = cv.CreateMat(1, 4, cv.CV_32F)
        rvecs = cv.CreateMat(1, 9, cv.CV_32F)
        tvecs = cv.CreateMat(1, 3, cv.CV_32F)
        pointArr = numpy.array([(x, y, 0) for y in xrange(PAT_SIZE[1]) for x in xrange(PAT_SIZE[0])], numpy.float32)
        objectPoints = cv.fromarray(pointArr)
        imgPointArr = numpy.array(corners, numpy.float32)
        imagePoints = cv.fromarray(imgPointArr)
        pointCounts = cv.CreateMat(1, 1, cv.CV_32S)
        pointCounts[0, 0] = PAT_SIZE[0] * PAT_SIZE[1]
        cv.CalibrateCamera2(objectPoints, imagePoints, pointCounts, IMG_SIZE, cam_matrix, dist_coeff, rvecs, tvecs)
        print "TVecs:", numpy.asarray(tvecs)
        rmat = numpy.asarray(rvecs).reshape((3, 3), order='C')
        print "RVecs:"
        print rmat
        # print "Azimuth:", rmat.dot(numpy.array([0, 0, 1]))
        # time.sleep(1)
        #import pdb; pdb.set_trace()
    else:
        cv.PutText(im, "Not found.", infoOrigin, infoFont, (0, 255, 0))
    return cv2pygame(im)

fps = 30.0
pygame.init()
window = pygame.display.set_mode(IMG_SIZE)
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
    screen.blit(pg_img, (0, 0))
    pygame.display.flip()
    # pygame.time.delay(int(1000 * 1.0/fps))
